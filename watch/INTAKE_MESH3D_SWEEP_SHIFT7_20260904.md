# INTAKE CARD — MESH3D NIGHT SWEEP (shift 7, 2026-09-04 ~08:01 EDT)

## SWEEP
Query: signed distance fields SDF rendering marching cubes mesh extraction technique news 2026.
Result: evergreen SDF reference material, plus one genuinely new research find.

## FINDINGS (tri-stated)

**1. Power Diagram Enhanced Adaptive Isosurface Extraction (arXiv 2506.09579, 2025).**
State-of-the-art evolution of mesh extraction from SDFs beyond Marching Cubes —
uses power diagrams for high-fidelity mesh surfaces. **BUILD WINDOWED candidate
for the mesh-baker pipeline:** the B1 erosion line produces SDF fields; this is
the technique that extracts high-fidelity meshes from them for 3D printing,
export, or the Mesh3D deck. (Supported: arXiv paper exists, link verified.)

**2. MeshSDF – Differentiable Iso-Surface Extraction (NeurIPS 2020).**
Foundational technique bridging neural SDFs and mesh extraction — differentiable
iso-surface means gradient flow through mesh generation. Relevant to the QLoRA
campaign's deep-compile line if the fleet ever trains models that generate 3D
geometry. (Supported: NeurIPS proceedings page exists.)

**3. Evergreen reference material** (iq's raymarching, CG Stack Exchange,
GradientSpace tutorials). Already held on the shelf or directly derivable.
No action.

## VERDICT
One BUILD WINDOWED candidate (power-diagram isosurface for mesh-baker/B1),
one REMEMBER (MeshSDF differentiable extraction for the training arm), rest
already-held reference. Rotation: mesh3d done → glmwatch next. Burn: $0.
