# Threshold values for CI bottleneck detection

# Queue time seconds above which a build is considered to have a queue bottleneck
QUEUE_TIME_THRESHOLD = 300  # 5 minutes

# Execution time seconds above which a task is considered slow
EXECUTION_TIME_THRESHOLD = 600  # 10 minutes

# Cache hit rate below which cache utilisation is considered poor (percentage)
CACHE_HIT_RATE_THRESHOLD = 0.6

# Agent utilisation below which agent contention is flagged (percentage)
AGENT_UTILISATION_THRESHOLD = 0.7

# Parallelisation inefficiency threshold (e.g., tasks that could be parallel but aren't)
PARALLELISATION_EFFICIENCY_THRESHOLD = 0.8
