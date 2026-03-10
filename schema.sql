CREATE TABLE data_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kernel_type TEXT NOT NULL,
    params TEXT NOT NULL,           -- JSON dict of kernel params
    score REAL NOT NULL,
    bandwidth_gb_s REAL,
    duration_us REAL,
    gpu_busy_pct REAL,
    occupancy_pct REAL,
    l2_hit_rate REAL,
    lds_stall_pct REAL,
    mem_unit_busy_pct REAL,
    write_stall_pct REAL,
    lds_bank_conflicts REAL,
    fetch_size_kb REAL,
    write_size_kb REAL,
    vgpr_count INTEGER,
    sgpr_count INTEGER,
    lds_size INTEGER,
    counters TEXT,                  -- JSON dict of raw counters
    kernel_output TEXT,             -- JSON dict of all kernel binary output
    timestamp TEXT NOT NULL,
    iteration INTEGER
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE invariants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,             -- cliff, plateau, sweet_spot, boundary
    kernel_type TEXT NOT NULL,
    description TEXT NOT NULL,
    param_axis TEXT,                -- Which parameter triggers the invariant
    threshold_value REAL,           -- Where it occurs
    magnitude REAL,                 -- How big the effect is
    confidence REAL,                -- How many data points support it
    evidence TEXT,                  -- JSON list of supporting data point IDs
    timestamp TEXT NOT NULL
);
CREATE TABLE discovery_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT NOT NULL,
    end_time TEXT,
    kernel_types TEXT,              -- JSON list
    iterations INTEGER,
    variants_tested INTEGER,
    invariants_found INTEGER,
    config TEXT                     -- JSON config snapshot
);
CREATE INDEX idx_dp_kernel ON data_points(kernel_type);
CREATE INDEX idx_dp_score ON data_points(score);
CREATE INDEX idx_inv_type ON invariants(type);
CREATE INDEX idx_inv_kernel ON invariants(kernel_type);
