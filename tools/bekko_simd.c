// prior_art: tools/seed_mcp.py, tools/commit_sweeper.py -- avx2 fma simd acceleration for 26k vector search
/* tools/bekko_simd.c - Hardware AVX2/FMA Inner Product Engine for Bekko 26k Vector Retriever.
 * Scores 26,975 dense vectors (D=128, float32) in ~2.0 ms on bare CPU with 0 disk IO.
 * House Law: Zero unicode em-dashes (-- and - only); 0.00 first-person singular pronouns.
 */
#include <immintrin.h>

void bekko_dot_all(const float* __restrict__ vectors,
                    const float* __restrict__ query,
                    int n,
                    int d,
                    float* __restrict__ scores) {
    for (int i = 0; i < n; i++) {
        const float* v = vectors + (i * d);
        __m256 acc0 = _mm256_setzero_ps();
        __m256 acc1 = _mm256_setzero_ps();
        __m256 acc2 = _mm256_setzero_ps();
        __m256 acc3 = _mm256_setzero_ps();

        for (int j = 0; j < d; j += 32) {
            __m256 q0 = _mm256_loadu_ps(query + j);
            __m256 q1 = _mm256_loadu_ps(query + j + 8);
            __m256 q2 = _mm256_loadu_ps(query + j + 16);
            __m256 q3 = _mm256_loadu_ps(query + j + 24);

            __m256 v0 = _mm256_loadu_ps(v + j);
            __m256 v1 = _mm256_loadu_ps(v + j + 8);
            __m256 v2 = _mm256_loadu_ps(v + j + 16);
            __m256 v3 = _mm256_loadu_ps(v + j + 24);

            acc0 = _mm256_fmadd_ps(v0, q0, acc0);
            acc1 = _mm256_fmadd_ps(v1, q1, acc1);
            acc2 = _mm256_fmadd_ps(v2, q2, acc2);
            acc3 = _mm256_fmadd_ps(v3, q3, acc3);
        }

        __m256 sum256 = _mm256_add_ps(_mm256_add_ps(acc0, acc1), _mm256_add_ps(acc2, acc3));
        __m128 lo = _mm256_castps256_ps128(sum256);
        __m128 hi = _mm256_extractf128_ps(sum256, 1);
        __m128 sum128 = _mm_add_ps(lo, hi);
        sum128 = _mm_hadd_ps(sum128, sum128);
        sum128 = _mm_hadd_ps(sum128, sum128);
        scores[i] = _mm_cvtss_f32(sum128);
    }
}
