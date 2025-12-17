"""
CONFIDENCE SCORER: Enhanced confidence scoring for Phase 11 operations.

Uses weighted scoring across pipeline stages to produce deterministic,
granular confidence scores that accurately reflect operation reliability.

WEIGHTS (Deterministic & Documented):
- Intent matching: 25% (how well intents matched natural language)
- Target component: 20% (how confident we are about target component)
- Field validity: 20% (how valid the modified fields are)
- Safety pass: 25% (how many safety checks passed)
- Penalty factors: -5% per ambiguity, -10% per warning
- Boost factors: +5% for exact match, +5% for single-intent, +3% for no warnings
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ConfidenceStage(Enum):
    """Pipeline stages for confidence tracking."""
    INTENT_PARSING = "intent_parsing"
    TARGET_RESOLUTION = "target_resolution"
    FIELD_VALIDITY = "field_validity"
    SAFETY_VERIFICATION = "safety_verification"
    FINAL_SCORING = "final_scoring"


@dataclass
class StageConfidence:
    """Confidence score for a single pipeline stage."""
    stage: ConfidenceStage
    score: float  # 0.0 to 1.0
    reason: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfidenceReport:
    """Complete confidence analysis with stage-by-stage breakdown."""
    final_score: float  # 0.0 to 1.0
    stage_scores: List[StageConfidence]
    penalties: List[Tuple[str, float]]  # (reason, amount)
    boosts: List[Tuple[str, float]]  # (reason, amount)
    explanation: str


class ConfidenceScorer:
    """Deterministic confidence scoring with weighted pipeline stages."""
    
    # STAGE WEIGHTS (Documented) - Sum must equal 1.0
    WEIGHTS = {
        "intent_matching": 0.25,
        "target_component": 0.20,
        "field_validity": 0.30,
        "safety_verification": 0.25,
    }
    
    # PENALTY & BOOST FACTORS (Documented)
    PENALTY_AMBIGUOUS_TARGET = 0.05
    PENALTY_PARTIAL_MATCH = 0.08
    PENALTY_WARNING = 0.05
    PENALTY_HIGH_RISK = 0.10
    
    BOOST_EXACT_MATCH = 0.05
    BOOST_SINGLE_INTENT = 0.03
    BOOST_ZERO_WARNINGS = 0.03
    
    def score(
        self,
        command: str,
        intents: List[Any],
        original_blueprint: Dict[str, Any],
        modified_blueprint: Dict[str, Any],
        patches: List[Any],
        simulation_result: Optional[Any] = None,
        verification_result: Optional[Any] = None,
    ) -> ConfidenceReport:
        """
        Calculate comprehensive confidence score with deterministic stage-by-stage analysis.
        
        Args:
            command: Original user command
            intents: Extracted intents
            original_blueprint: Original state
            modified_blueprint: Modified state
            patches: Applied patches
            simulation_result: Result from simulator
            verification_result: Result from verifier
        
        Returns:
            ConfidenceReport with final score and detailed breakdown
        """
        stage_scores: List[StageConfidence] = []
        penalties: List[Tuple[str, float]] = []
        boosts: List[Tuple[str, float]] = []
        
        # STAGE 1: INTENT PARSING CONFIDENCE
        intent_conf = self._score_intent_parsing(intents, command)
        stage_scores.append(intent_conf)
        
        # STAGE 2: TARGET COMPONENT CONFIDENCE
        target_conf = self._score_target_resolution(intents, original_blueprint)
        stage_scores.append(target_conf)
        
        # STAGE 3: FIELD VALIDITY CONFIDENCE
        field_conf = self._score_field_validity(patches, intents)
        stage_scores.append(field_conf)
        
        # STAGE 4: SAFETY VERIFICATION CONFIDENCE
        safety_conf = self._score_safety_verification(
            simulation_result,
            verification_result
        )
        stage_scores.append(safety_conf)
        
        # CALCULATE WEIGHTED SCORE
        weighted_score = (
            intent_conf.score * self.WEIGHTS["intent_matching"] +
            target_conf.score * self.WEIGHTS["target_component"] +
            field_conf.score * self.WEIGHTS["field_validity"] +
            safety_conf.score * self.WEIGHTS["safety_verification"]
        )
        
        # APPLY PENALTIES
        if self._has_ambiguous_targeting(intents):
            penalty = self.PENALTY_AMBIGUOUS_TARGET
            penalties.append(("Ambiguous component targeting", penalty))
            weighted_score -= penalty
        
        if self._has_partial_match(intents):
            penalty = self.PENALTY_PARTIAL_MATCH
            penalties.append(("Partial intent matching", penalty))
            weighted_score -= penalty
        
        if simulation_result and simulation_result.warnings:
            warning_penalty = len(simulation_result.warnings) * self.PENALTY_WARNING
            penalties.append((f"{len(simulation_result.warnings)} simulation warnings", warning_penalty))
            weighted_score -= warning_penalty
        
        if simulation_result and simulation_result.risk_score > 0.3:
            high_risk_penalty = self.PENALTY_HIGH_RISK
            penalties.append(("High simulation risk score", high_risk_penalty))
            weighted_score -= high_risk_penalty
        
        # APPLY BOOSTS
        if len(intents) == 1:
            boost = self.BOOST_SINGLE_INTENT
            boosts.append(("Single-intent command", boost))
            weighted_score += boost
        
        if self._is_exact_component_match(intents, original_blueprint):
            boost = self.BOOST_EXACT_MATCH
            boosts.append(("Exact component ID match", boost))
            weighted_score += boost
        
        if simulation_result and not simulation_result.warnings:
            boost = self.BOOST_ZERO_WARNINGS
            boosts.append(("Zero simulation warnings", boost))
            weighted_score += boost
        
        # CLAMP TO VALID RANGE
        final_score = max(0.0, min(1.0, weighted_score))
        
        # BUILD EXPLANATION
        explanation = self._build_explanation(
            stage_scores,
            penalties,
            boosts,
            final_score,
            intents,
            simulation_result
        )
        
        return ConfidenceReport(
            final_score=final_score,
            stage_scores=stage_scores,
            penalties=penalties,
            boosts=boosts,
            explanation=explanation
        )
    
    def _score_intent_parsing(self, intents: List[Any], command: str) -> StageConfidence:
        """Score quality of intent parsing."""
        if not intents:
            return StageConfidence(
                stage=ConfidenceStage.INTENT_PARSING,
                score=0.0,
                reason="No intents parsed from command",
                details={"command": command}
            )
        
        # Average confidence across all intents
        total_confidence = 0.0
        for intent in intents:
            total_confidence += getattr(intent, "confidence", 0.85)
        
        avg_confidence = total_confidence / len(intents)
        
        # Penalize if intents look uncertain
        if avg_confidence < 0.7:
            score = avg_confidence * 0.8  # Confidence penalty for uncertain intents
        else:
            score = avg_confidence
        
        return StageConfidence(
            stage=ConfidenceStage.INTENT_PARSING,
            score=score,
            reason=f"Parsed {len(intents)} intent(s) with avg confidence {avg_confidence:.2f}",
            details={
                "intent_count": len(intents),
                "avg_confidence": avg_confidence,
                "intent_types": [str(i.type) for i in intents]
            }
        )
    
    def _score_target_resolution(
        self,
        intents: List[Any],
        blueprint: Dict[str, Any]
    ) -> StageConfidence:
        """Score accuracy of target component resolution."""
        if not intents:
            return StageConfidence(
                stage=ConfidenceStage.TARGET_RESOLUTION,
                score=0.0,
                reason="No intents to resolve",
            )
        
        score = 0.9  # Default high confidence
        targets_resolved = 0
        targets_ambiguous = 0
        targets_missing = 0
        
        components = blueprint.get("components", [])
        component_types = [c.get("type") for c in components]
        
        for intent in intents:
            target = getattr(intent, "target", None)
            
            if target is None:
                targets_missing += 1
                score -= 0.05
            elif target in ["button", "navbar", "text", "container", "product"]:
                # Check if target exists in blueprint
                if target in component_types or len(components) > 0:
                    targets_resolved += 1
                else:
                    targets_missing += 1
                    score -= 0.10
            elif target in component_types:
                # Exact match
                targets_resolved += 1
            else:
                # Possible ambiguity
                targets_ambiguous += 1
                score -= 0.08
        
        score = max(0.0, min(1.0, score))
        
        return StageConfidence(
            stage=ConfidenceStage.TARGET_RESOLUTION,
            score=score,
            reason=f"Resolved {targets_resolved} target(s), {targets_ambiguous} ambiguous, {targets_missing} missing",
            details={
                "resolved": targets_resolved,
                "ambiguous": targets_ambiguous,
                "missing": targets_missing,
                "total_components": len(components)
            }
        )
    
    def _score_field_validity(self, patches: List[Any], intents: List[Any]) -> StageConfidence:
        """Score validity of field modifications."""
        if not patches:
            return StageConfidence(
                stage=ConfidenceStage.FIELD_VALIDITY,
                score=0.5,
                reason="No patches to validate",
            )
        
        valid_paths = 0
        invalid_paths = 0
        
        # Whitelisted safe paths
        SAFE_PATHS = {
            "/tokens/",
            "/components/",
            "/visual/",
            "/bbox",
            "/text",
            "/color",
            "/bg_color",
            "/height",
            "/width",
            "/font_weight",
            "/font_style",
            "/box_shadow",
            "/border_radius"
        }
        
        for patch in patches:
            path = getattr(patch, "path", "")
            is_safe = any(safe_path in path for safe_path in SAFE_PATHS)
            
            if is_safe:
                valid_paths += 1
            else:
                invalid_paths += 1
        
        if invalid_paths > 0:
            score = valid_paths / (valid_paths + invalid_paths) * 0.8
        else:
            score = min(1.0, (valid_paths / max(1, len(intents))) * 0.95)
        
        return StageConfidence(
            stage=ConfidenceStage.FIELD_VALIDITY,
            score=score,
            reason=f"All {valid_paths} patch(es) target whitelisted fields",
            details={
                "valid_patches": valid_paths,
                "invalid_patches": invalid_paths,
                "total_patches": len(patches)
            }
        )
    
    def _score_safety_verification(
        self,
        simulation_result: Optional[Any] = None,
        verification_result: Optional[Any] = None
    ) -> StageConfidence:
        """Score safety verification outcomes."""
        score = 0.5
        details = {}
        reason = "No safety data available"
        
        if simulation_result:
            if simulation_result.safe:
                score = 0.95
                reason = f"Simulation passed with risk score {simulation_result.risk_score:.2f}"
            else:
                score = 0.3
                reason = f"Simulation failed: {simulation_result.reason}"
            
            details["simulation_safe"] = simulation_result.safe
            details["risk_score"] = simulation_result.risk_score
            details["warnings"] = len(simulation_result.warnings)
        
        if verification_result:
            if verification_result.valid:
                score = min(1.0, score + 0.05)
                reason += " + verification passed"
            else:
                score = min(0.3, score - 0.1)
                reason += f" + verification failed ({len(verification_result.errors)} errors)"
            
            details["verification_valid"] = verification_result.valid
            details["verification_errors"] = len(verification_result.errors)
            details["verification_warnings"] = len(verification_result.warnings)
        
        score = max(0.0, min(1.0, score))
        
        return StageConfidence(
            stage=ConfidenceStage.SAFETY_VERIFICATION,
            score=score,
            reason=reason,
            details=details
        )
    
    def _has_ambiguous_targeting(self, intents: List[Any]) -> bool:
        """Check if any intent has ambiguous component targeting."""
        for intent in intents:
            target = getattr(intent, "target", None)
            # Ambiguous if target is None or generic type with multiple possible matches
            if target is None:
                return True
        return False
    
    def _has_partial_match(self, intents: List[Any]) -> bool:
        """Check if intents show partial/fuzzy matching."""
        for intent in intents:
            confidence = getattr(intent, "confidence", 1.0)
            if confidence < 0.75:
                return True
        return False
    
    def _is_exact_component_match(self, intents: List[Any], blueprint: Dict[str, Any]) -> bool:
        """Check if intents match exact component IDs."""
        if not intents:
            return False
        
        components = blueprint.get("components", [])
        component_ids = [c.get("id") for c in components]
        
        # Check if any intent targets an exact component ID
        for intent in intents:
            target = getattr(intent, "target", None)
            if target and target in component_ids:
                return True
        
        return False
    
    def _build_explanation(
        self,
        stage_scores: List[StageConfidence],
        penalties: List[Tuple[str, float]],
        boosts: List[Tuple[str, float]],
        final_score: float,
        intents: List[Any],
        simulation_result: Optional[Any]
    ) -> str:
        """Build human-readable confidence explanation."""
        lines = []
        
        lines.append(f"Confidence Score: {final_score:.1%}")
        lines.append("")
        
        lines.append("Pipeline Stage Analysis:")
        for stage in stage_scores:
            lines.append(f"  {stage.stage.value}: {stage.score:.1%} - {stage.reason}")
        
        if penalties:
            lines.append("")
            lines.append("Penalties Applied:")
            for reason, amount in penalties:
                lines.append(f"  -{amount:.1%}: {reason}")
        
        if boosts:
            lines.append("")
            lines.append("Bonuses Applied:")
            for reason, amount in boosts:
                lines.append(f"  +{amount:.1%}: {reason}")
        
        # Overall assessment
        lines.append("")
        if final_score >= 0.90:
            assessment = "Highly Confident - Safe to apply"
        elif final_score >= 0.75:
            assessment = "Confident - Proceed with caution"
        elif final_score >= 0.60:
            assessment = "Moderate Confidence - Review recommended"
        else:
            assessment = "Low Confidence - Manual review required"
        
        lines.append(f"Assessment: {assessment}")
        
        return "\n".join(lines)
