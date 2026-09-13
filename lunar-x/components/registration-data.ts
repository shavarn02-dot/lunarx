export interface ImagePair { id: string; name: string; source: string; reference: string; sensor: string; description: string }
export const PAIRS: ImagePair[] = [
  { id: 'default', name: 'TMC-2 crater scene', source: 'ch2_tmc_crater_scene_src.png', reference: 'ch2_tmc_crater_scene_ref.png', sensor: 'TMC-2', description: 'Two observations of the same lunar terrain, ready for alignment.' },
  { id: 'cross', name: 'OHRC × TMC-2 overlap', source: 'ch2_ohr_ncp_overlap_patch.jpg', reference: 'ch2_tmc_ncn_patch_crop.jpg', sensor: 'OHRC / TMC-2', description: 'Compare an overlapping region captured by two different sensors.' },
  ...['Alpha', 'Beta', 'Gamma', 'Delta'].map(name => ({ id: name.toLowerCase(), name: `Crater region ${name}`, source: `Pair_Crater_Region_${name}_SRC.png`, reference: `Pair_Crater_Region_${name}_REF.png`, sensor: 'TMC-2', description: 'A paired lunar terrain sample from the project image collection.' })),
]
export interface Settings { method: string; preprocessing: string; model_type: string; subpixel: boolean; spatial_filter: boolean; reproj_thresh: number }
export const DEFAULT_SETTINGS: Settings = { method: 'sift', preprocessing: 'clahe', model_type: 'affine', subpixel: true, spatial_filter: true, reproj_thresh: 3 }
export interface Metrics { inliers: number; inlier_ratio_pct: number; reproj_rmse_coarse: number; reproj_rmse_refined: number; spatial_coverage_pct: number; status: string }
export interface Benchmark extends Metrics { source: string; reference: string; method: string; preprocessing: string; runtime_sec: number }
export interface RegistrationResult { success: boolean; runtime_sec: number; metrics: Metrics; images: { matches: string; registered: string; checkerboard: string; difference: string }; error?: string; logs?: string[]; transformation_matrix?: number[][]; provenance: 'saved' | 'live'; pairName: string; method: string; preprocessing: string }
export function imageUrl(filename: string) { return `/api/images/${encodeURIComponent(filename.split('/').pop() || '')}` }
export function downloadReport(result: RegistrationResult) {
  const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = `chandra-sync-${result.provenance}-report.json`
  anchor.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
