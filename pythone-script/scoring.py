def scoring_system(metrics: dict) -> tuple[float, dict [str, float]] :
      """
        Evaluates the processing result of a file and calculates a score.
        
        Args:
            result (dict): Data containing metrics like long function and unused import.
            
        Returns:
            tuple: (total_score, score_breakdown)
        """

Weights = {
      "long_function": 5
}