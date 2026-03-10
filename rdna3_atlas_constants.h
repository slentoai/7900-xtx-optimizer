// Auto-generated from rdna3-discovery atlas
// Generated: 2026-03-05T00:35:17.213520
// Source: 100% parameter space coverage of RX 7900 XTX (gfx1100)
#pragma once
#include <cstddef>

namespace rdna3_atlas {

// Memory hierarchy (discovered)
constexpr int INFINITY_CACHE_MB = 96;
constexpr double PEAK_CACHED_BW_GBS = 2561.6;
constexpr double DRAM_BW_GBS = 2043.5;
constexpr double CACHE_TO_DRAM_RATIO = 1.25;

// LDS characteristics (discovered)
constexpr int LDS_NUM_BANKS = 32;
constexpr int LDS_BANK_WIDTH_BYTES = 4;
constexpr double PEAK_LDS_BW_GBS = 1420.0;
constexpr double LDS_CONFLICT_PENALTY_PCT = 86.6;

// Optimal LDS strides (bank-conflict-free, discovered)
constexpr int BEST_LDS_STRIDES[] = {1, 2, 21, 22, 23};
constexpr int WORST_LDS_STRIDES[] = {32};

// Block size recommendations (discovered)
constexpr int OPTIMAL_BLOCK_SIZE = 128;
constexpr int OPTIMAL_ELEMENTS_PER_THREAD = 2;
constexpr int WAVE_SIZE = 32;

// Architecture constants
constexpr int COMPUTE_UNITS = 96;
constexpr int LDS_PER_CU_KB = 128;
constexpr double GPU_CLOCK_GHZ = 2.5;
constexpr double PEAK_FP32_TFLOPS = 61.4;
constexpr double PEAK_MEM_BW_GBS = 960.0;


// Compute ILP characteristics (discovered)
constexpr int OPTIMAL_FP32_FMA_CHAINS = 7;
constexpr int OPTIMAL_FP32_BLOCK_SIZE = 512;
constexpr double ACHIEVED_FP32_TFLOPS = 50.06;
constexpr double FP32_ILP_SPEEDUP = 2.33;
constexpr int OPTIMAL_FP16_HALF2_CHAINS = 11;
constexpr int OPTIMAL_FP16_BLOCK_SIZE = 1024;
constexpr double ACHIEVED_FP16_TFLOPS = 57.92;
constexpr double FP16_ILP_SPEEDUP = 1.04;

// Reduction kernel (discovered)
constexpr int OPTIMAL_REDUCTION_BLOCK_SIZE = 512;
constexpr int OPTIMAL_ITEMS_PER_THREAD = 7;

// Tiled GEMM (discovered)
constexpr int OPTIMAL_TILE_M = 128;
constexpr int OPTIMAL_TILE_N = 128;

// Wave scheduling (discovered)
constexpr int OPTIMAL_WAVES_PER_CU = 31;
constexpr int OPTIMAL_OCCUPANCY_PCT = 95;

// WMMA matrix operations (discovered)
constexpr int WMMA_TILE_SIZE = 16;  // 16x16x16 per instruction
constexpr int OPTIMAL_WMMA_K_TILES = 34;
constexpr int OPTIMAL_WMMA_CHAINS = 6;
constexpr double PEAK_WMMA_TFLOPS = 88.76;

// Atomic operations (discovered)
constexpr double PEAK_ATOMIC_GOPS = 431.38;
constexpr double CONTENDED_ATOMIC_GOPS = 2.88;
constexpr int OPTIMAL_ATOMIC_BLOCK_SIZE = 1024;

// Compute-memory overlap / roofline (discovered)
constexpr int ROOFLINE_KNEE_INTENSITY = 1;
constexpr double PEAK_OVERLAP_BW_GBS = 1891.0;

// Helper: is this stride likely to cause LDS bank conflicts?
inline bool has_lds_bank_conflict(int stride) {
    return (stride % LDS_NUM_BANKS) == 0;
}

// Helper: should this working set tile into Infinity Cache?
inline bool fits_infinity_cache(size_t bytes) {
    return bytes <= 96ULL * 1024 * 1024;
}

} // namespace rdna3_atlas
