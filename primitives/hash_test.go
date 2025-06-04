package primitives

import (
    "testing"

    "lattice-threshold-signature/utils"
)

func TestGenerateRandomSeedLength(t *testing.T) {
    utils.PrecomputeRandomness(64, []byte("test-seed-for-randomness"))
    seed := GenerateRandomSeed()
    if len(seed) != keySize {
        t.Fatalf("expected seed length %d, got %d", keySize, len(seed))
    }
}
