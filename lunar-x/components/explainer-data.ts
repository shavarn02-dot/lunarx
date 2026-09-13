export interface ExplainerItem {
  title: string;
  whatItDoes: string;
  projectRole: string;
  keywords?: string[];
}

export const EXPLAINER_DICT: Record<string, ExplainerItem> = {
  // --- METRICS ROW ---
  reproj_rmse: {
    title: "Reprojection RMSE (Root Mean Square Error)",
    whatItDoes:
      "Ye measure karta hai ki source image ke crater points transform hone ke baad reference image ke original points se kitne pixel door reh gaye. Jitna kam hoga, alignment utni hi accurate hoti hai!",
    projectRole:
      "ISRO ka strict mandate hai ki geometric residual < 1.0 pixel hona chahiye. Humara pipeline 0.148 px achieve karta hai jo sub-pixel level geometric accuracy ensure karta hai!",
    keywords: ["crater points", "Jitna kam hoga", "residual < 1.0 pixel", "0.148 px", "sub-pixel level geometric accuracy"]
  },
  verified_inliers: {
    title: "Verified Inliers (Sahi Tie-Points)",
    whatItDoes:
      "Feature matching ke dauraan bohot saare fake ya duplicate matches nikalte hain. Inliers wahi points hote hain jo USAC_MAGSAC algorithm ne mathematically 100% genuine verify kiye hain.",
    projectRole:
      "Lunar surface par 1,329 rock-solid inliers milne se image registration poori tarah trustworthy ho jaati hai, koi bhi false tie-point bacha nahi rehta.",
    keywords: ["fake ya duplicate matches", "100% genuine verify", "1,329 rock-solid inliers", "trustworthy"]
  },
  inlier_ratio: {
    title: "Inlier Ratio (% Genuine Matches)",
    whatItDoes:
      "Total dhoondhe gaye matches mein se kitne percent matches genuinely sach nikle, ye uska ratio calculate karta hai.",
    projectRole:
      "Humara system 99.85% inlier ratio deta hai (1331 mein se 1329 correct!), matlab false match ka risk bilkul zero ho gaya hai.",
    keywords: ["kitne percent matches", "99.85% inlier ratio", "1329 correct", "zero ho gaya"]
  },
  spatial_coverage: {
    title: "Spatial Coverage (8x8 Grid Spread)",
    whatItDoes:
      "Ye check karta hai ki tie-points poori lunar image par failay hue hain ya kisi ek crater ke kone mein jama ho gaye hain.",
    projectRole:
      "Hum image ko 8x8 (64 bins) mein divide karke 96.12% coverage ensure karte hain, taaki poora lunar map charo taraf se barabar align ho.",
    keywords: ["poori lunar image par", "8x8 (64 bins)", "96.12% coverage", "charo taraf se barabar"]
  },
  processing_time: {
    title: "Processing Latency (Execution Speed)",
    whatItDoes:
      "Raw satellite images ko load karne se lekar features match karke final warped image banane mein laga kul waqt.",
    projectRole:
      "FastAPI aur optimized C++ OpenCV backend se ye poori complex calculation sirf 0.159 seconds mein complete ho jaati hai, real-time satellite ops ke liye perfect.",
    keywords: ["kul waqt", "FastAPI", "0.159 seconds", "real-time satellite ops"]
  },
  registration_status: {
    title: "Registration Status (Pipeline Acceptance)",
    whatItDoes:
      "Ye final verdict deta hai ki dono images successfully lock ho gayi hain ya unme koi geometric mismatch hai.",
    projectRole:
      "Jab ISRO benchmark (RMSE < 1.0 px aur >70% coverage) satisfy hota hai, tabhi ye status 'Successful' declare karta hai.",
    keywords: ["final verdict", "RMSE < 1.0 px", ">70% coverage", "Successful"]
  },

  // --- REGISTRATION CONTROLS & ALGORITHMS ---
  feature_matcher: {
    title: "Feature Matcher (Crater Landmark Detector)",
    whatItDoes:
      "Dono alag-alag orbital images mein se unique pahad, crater rims, aur boulders ke distinctive landmarks dhoondhne wala engine.",
    projectRole:
      "Chandrayaan-2 ke alag orbits mein sun ki roshni alag angle se aati hai, feature matcher lighting ke bawajood same craters ko identify karta hai.",
    keywords: ["distinctive landmarks", "sun ki roshni alag angle", "same craters"]
  },
  sift: {
    title: "SIFT (Scale-Invariant Feature Transform)",
    whatItDoes:
      "Aisa robust algorithm jo image ko chhota, bada, ya ghumane par bhi uske crater corners aur gradients ko bina bhule pehchan leta hai.",
    projectRole:
      "Project ka primary baseline matcher hai, jo extreme solar angles mein 1,300+ solid tie-points nikaal kar deta hai.",
    keywords: ["chhota, bada, ya ghumane", "extreme solar angles", "1,300+ solid tie-points"]
  },
  orb: {
    title: "ORB (Oriented FAST and Rotated BRIEF)",
    whatItDoes:
      "Ek ultra-fast binary descriptor jo bohot kam memory aur compute power mein rapid corners detect karta hai.",
    projectRole:
      "Low-power onboard satellite computers ya real-time lightweight edge devices ke liye alternative fast matching option hai.",
    keywords: ["ultra-fast binary descriptor", "kam memory", "onboard satellite computers"]
  },
  superpoint_lightglue: {
    title: "SuperPoint + LightGlue (Deep Neural Matcher)",
    whatItDoes:
      "Deep Learning neural network jo crater features extract karta hai aur Transformer attention mechanism se unhe aapas mein glue karta hai.",
    projectRole:
      "Jab craters ke andar bohot kaala andhera (harsh shadow) ho, tab ye AI model un hidden features ko bhi accurately connect kar leta hai.",
    keywords: ["Deep Learning neural network", "Transformer attention", "kaala andhera", "accurately connect"]
  },
  loftr: {
    title: "LoFTR (Detector-Free Transformer Matching)",
    whatItDoes:
      "Bina kisi corner point ka intezar kiye, poori image par continuous dense feature grid match karta hai.",
    projectRole:
      "Lunar South Pole ke flat terrain ya low-texture scenes mein jahan normal features nahi milte, wahan LoFTR sub-pixel matches nikaalta hai.",
    keywords: ["Bina corner point", "dense feature grid", "South Pole", "low-texture scenes"]
  },
  preprocessing: {
    title: "Image Preprocessing (Shadow & Noise Handling)",
    whatItDoes:
      "Features dhoondhne se pehle raw satellite image ko saaf aur contrast enhance karne ka visual filter.",
    projectRole:
      "Moon par koi atmosphere nahi hota, isliye dhoop bohot tez aur chhaon bohot kaali hoti hai; preprocessing lighting differences ko balance karti hai.",
    keywords: ["contrast enhance", "koi atmosphere nahi hota", "lighting differences ko balance"]
  },
  clahe: {
    title: "CLAHE (Contrast Limited Adaptive Histogram Equalization)",
    whatItDoes:
      "Image ko chhote-chhote tiles mein baant kar har tile ka contrast alag se boost karta hai, taaki noise bina badhe details ubhar sakein.",
    projectRole:
      "Chandrayaan-2 TMC-2 ke crater floors ke andar chhupe hue fine rocks aur ridges ko clearly visible bana deta hai.",
    keywords: ["chhote-chhote tiles", "contrast alag se boost", "crater floors", "ridges ko clearly visible"]
  },
  gradient: {
    title: "Gradient Preprocessing (Sobel Edge Filtering)",
    whatItDoes:
      "Image se flat surface hata kar sirf crater rims aur ridges ki sharp boundary lines nikalta hai.",
    projectRole:
      "Suraj ki roshni kitni bhi badle, crater ki physical boundary wahi rehti hai; gradient filter se matcher lighting se confuse nahi hota.",
    keywords: ["sharp boundary lines", "Suraj ki roshni", "confuse nahi hota"]
  },
  phase_congruency: {
    title: "Phase Congruency (Illumination Invariant)",
    whatItDoes:
      "Fourier frequency domain mein jaakar local phase match karta hai jo brightness aur contrast variations se 100% immune hota hai.",
    projectRole:
      "Terminator line (day-night boundary) par li gayi lunar images ko match karne ka ultimate scientific weapon hai.",
    keywords: ["Fourier frequency", "100% immune", "Terminator line"]
  },
  transformation: {
    title: "Transformation Model (Geometric Warping)",
    whatItDoes:
      "Wo mathematical formula (matrix) jo source image ko ghumata, khinchta, aur stretch karke reference frame par fit karta hai.",
    projectRole:
      "Satellite ke orbital tilt aur flight path difference ko physically correct karke dono images ko ek hi coordinate grid par le aata hai.",
    keywords: ["mathematical formula", "reference frame par fit", "orbital tilt", "ek hi coordinate grid"]
  },
  affine: {
    title: "Affine Model (6 Degrees of Freedom)",
    whatItDoes:
      "Translation (X, Y shift), Rotation, Zoom (Scale), aur Skew (Shear) ko handle karne wala 2x3 linear matrix model.",
    projectRole:
      "Chandrayaan-2 TMC-2 push-broom sensors ke cross-pass alignment ke liye ISRO recommended standard model hai.",
    keywords: ["Translation, Rotation, Scale, Shear", "2x3 linear matrix", "ISRO recommended"]
  },
  homography: {
    title: "Homography Model (8 Degrees of Freedom)",
    whatItDoes:
      "Perspective tilt aur 3D angle differences ko adjust karne wala 3x3 projective matrix model.",
    projectRole:
      "Jab satellite camera seedha neeche dekhne ke bajaye thoda tirchha (oblique) angle se picture leta hai, tab homography perspective warp theek karti hai.",
    keywords: ["Perspective tilt", "3x3 projective matrix", "tirchha (oblique) angle"]
  },
  rigid: {
    title: "Rigid / Euclidean Model (3 Degrees of Freedom)",
    whatItDoes:
      "Sirf shift (X, Y) aur rotation allow karta hai, image ka size ya aakar bilkul change nahi hone deta.",
    projectRole:
      "Same altitude aur identical lens focal length wale passes mein fast aur constrained baseline matching ke liye useful hai.",
    keywords: ["shift aur rotation", "size ya aakar change nahi", "fast baseline matching"]
  },
  subpixel: {
    title: "Sub-Pixel Refinement (Fine Parabolic Fitting)",
    whatItDoes:
      "Normal computer pixels integer (1, 2, 3) hote hain. Sub-pixel refinement mathematical Taylor series se 0.01 pixel tak ka microscopic shift nikal leti hai.",
    projectRole:
      "ISRO ka strict criterion (<1.0 px) achieve karne ke liye coarse matrix ko 0.148 px tak razor-sharp bana deti hai.",
    keywords: ["0.01 pixel tak ka microscopic shift", "ISRO strict criterion", "0.148 px tak razor-sharp"]
  },
  spatial_filter_option: {
    title: "8x8 Spatial Coverage Validation Option",
    whatItDoes:
      "Image ko 64 blocks mein baant kar check karta hai ki inliers har disha mein evenly distributed hain ya nahi.",
    projectRole:
      "Agar saare matches kisi ek hi crater par chipak gaye to baaki moon ka hissa galat warp ho sakta hai; ye option poore frame ki safety ensure karta hai.",
    keywords: ["64 blocks", "evenly distributed", "poore frame ki safety"]
  },
  reproj_thresh_option: {
    title: "Reprojection Threshold (Inlier Cutoff Distance)",
    whatItDoes:
      "Wo maximum doori (pixels mein) jiske andar warped point aur reference point match karein tabhi use inlier maana jayega.",
    projectRole:
      "Default 3.0 px threshold par USAC_MAGSAC bad matches ko bahar fek deta hai aur true moon surface correspondences preserve karta hai.",
    keywords: ["maximum doori", "USAC_MAGSAC", "bad matches ko bahar", "true moon surface"]
  },
  run_registration_btn: {
    title: "Run Registration Action Button",
    whatItDoes:
      "Ye button dabate hi frontend backend API ko call karta hai aur poora autonomous registration workflow trigger ho jata hai.",
    projectRole:
      "FastAPI server par raw images bhejta hai, SIFT/MAGSAC run karwata hai aur sub-pixel metrics dashboard par display karta hai.",
    keywords: ["autonomous registration workflow", "FastAPI server", "sub-pixel metrics"]
  },

  // --- RESULT VIEWER TABS ---
  tab_overlay: {
    title: "Overlay Blend View",
    whatItDoes:
      "Dono images ko 50%-50% transparency ke sath ek doosre ke theek upar superimpose karke dikhata hai.",
    projectRole:
      "Aankhon se check karne ke liye ki dono orbital passes ke pahad aur gaddhe ek doosre ke upar perfectly match ho rahe hain.",
    keywords: ["50%-50% transparency", "superimpose", "perfectly match"]
  },
  tab_checkerboard: {
    title: "Checkerboard Inspection View (8x8 Grid)",
    whatItDoes:
      "Shatranj ke board ki tarah alternate blocks mein ek block source ka aur agla block reference ka render karta hai.",
    projectRole:
      "Judges ke liye sabse convincing visual proof! Crater ki gol boundary blocks ke beech bina kisi jhatke ya seam ke continuous dikhti hai.",
    keywords: ["Shatranj ke board", "Crater ki gol boundary", "continuous dikhti hai", "sub-pixel alignment"]
  },
  tab_matches: {
    title: "Match Vectors View (Tie-Point Lines)",
    whatItDoes:
      "Source crater points aur reference crater points ke beech green lines draw karke link dikhata hai.",
    projectRole:
      "Visualise karta hai ki 1,329 inliers poore lunar surface par uniformly linked hain aur lighting difference ke bawajood koi crossed/galat line nahi hai.",
    keywords: ["green lines", "1,329 inliers", "uniformly linked", "koi crossed line nahi"]
  },
  tab_difference: {
    title: "Residual Difference Heatmap (Error Map)",
    whatItDoes:
      "Aligned source aur reference image ka pixel-by-pixel subtraction karta hai using scientific JET colormap.",
    projectRole:
      "Deep blue color 0 geometric difference represent karta hai! Agar image galat judi hoti to red shadows aur ghosting dikhti.",
    keywords: ["pixel-by-pixel subtraction", "JET colormap", "Deep blue color = 0 geometric difference", "ghosting"]
  },
  tab_split: {
    title: "Split View Slider (Interactive Wipe Curtain)",
    whatItDoes:
      "Screen par ek interactive slider deta hai jise left-right drag karke dono images ko live compare kiya ja sakta hai.",
    projectRole:
      "ISRO scientists ko crater boundary aur elevation slope ka real-time visual audit karne ki suvidha deta hai.",
    keywords: ["interactive slider", "left-right drag", "crater boundary", "visual audit"]
  },

  // --- INPUT PAIRS & SENSORS ---
  source_image: {
    title: "Source Lunar Image (Unregistered)",
    whatItDoes:
      "Wo lunar image jise hume rotate, scale, aur warp karke reference map par fit karna hai.",
    projectRole:
      "Chandrayaan-2 TMC-2 Orbit 3922 se li gayi scene jisme sun ka angle alag hone ki wajah se shadows deep aur stretched hain.",
    keywords: ["warp karke reference map par fit", "TMC-2 Orbit 3922", "shadows deep"]
  },
  reference_image: {
    title: "Reference Lunar Image (Base Coordinate Frame)",
    whatItDoes:
      "Wo master lunar image jiske coordinate system ko sach maan kar source image ko uske upar fit kiya jata hai.",
    projectRole:
      "Chandrayaan-2 TMC-2 Orbit 3943 se li gayi baseline image jiska spatial geometry reference standard maana jata hai.",
    keywords: ["master lunar image", "coordinate system", "Orbit 3943", "reference standard"]
  },
  preset_pair: {
    title: "Preset Orbital Pair Loader",
    whatItDoes:
      "Chandrayaan-2 mission ke real lunar terrain data pairs ko ek click mein switch karne ka quick selector.",
    projectRole:
      "Presentation aur demo ke waqt bina kisi manual file upload ke real crater data instantly load karta hai.",
    keywords: ["real lunar terrain data", "ek click mein switch", "instantly load"]
  },
  tmc2_sensor: {
    title: "TMC-2 Sensor (Terrain Mapping Camera-2)",
    whatItDoes:
      "Chandrayaan-2 par laga 3-strip stereo camera jo 5.0 meters per pixel ki high resolution par moon ki surface capture karta hai.",
    projectRole:
      "Lunar surface ka high-precision digital elevation model (DEM) aur 3D terrain map banane ke liye primary image source.",
    keywords: ["5.0 meters per pixel", "stereo camera", "3D terrain map"]
  },
  provenance: {
    title: "Provenance & PDS4 Metadata",
    whatItDoes:
      "Data ki shuruaat, satellite orbit number, UTC timestamp, aur camera calibration parameters ka official planetary record.",
    projectRole:
      "ISRO ke Planetary Data System (PDS4) standards ke mutabiq scientific legitimacy confirm karta hai.",
    keywords: ["official planetary record", "PDS4 standards", "scientific legitimacy"]
  },

  // --- HEADER & SYSTEM CONTROLS ---
  system_state: {
    title: "System Online Status & Cloudflare Tunnel",
    whatItDoes:
      "Frontend aur local Python FastAPI backend ke beech live HTTPS connectivity monitor karta hai.",
    projectRole:
      "Cloudflare Zero-Trust Tunnel ke zariye secure sub-second connection maintain karta hai bina Render ke cold-start lag ke.",
    keywords: ["live HTTPS connectivity", "Cloudflare Zero-Trust Tunnel", "sub-second connection"]
  },
  export_report: {
    title: "Export Audit Report (CSV Dossier)",
    whatItDoes:
      "Run kiye gaye registration experiment ka poora math, transformation matrix, aur quality scores CSV file mein export karta hai.",
    projectRole:
      "ISRO judges aur evaluators ko mathematical proof submit karne ke liye one-click downloadable report.",
    keywords: ["transformation matrix", "quality scores", "one-click downloadable report"]
  },
  team_id_banner: {
    title: "SIH-2026 Problem Statement PS-26166",
    whatItDoes:
      "Smart India Hackathon 2026 ka official problem statement ID.",
    projectRole:
      "Chandrayaan-2: Sun & Scale-Invariant Lunar Matching - hamara project isi challenge ko sub-pixel level par solve karta hai.",
    keywords: ["Smart India Hackathon 2026", "Sun & Scale-Invariant Lunar Matching", "sub-pixel level"]
  },

  // --- QUALITY SUMMARY & ADVANCED DETAILS ---
  registration_quality: {
    title: "Automated Quality Verification Engine",
    whatItDoes:
      "Mathematical rules check karta hai: RMSE < 1.0 px, inliers > 100, coverage > 70%, condition number < 10^5.",
    projectRole:
      "Human intervention ke bina autonomously decide karta hai ki map ISRO navigation aur scientific research ke liye accept hoga ya reject.",
    keywords: ["RMSE < 1.0 px", "coverage > 70%", "Human intervention ke bina", "accept hoga ya reject"]
  },
  condition_number: {
    title: "Condition Number (SVD Matrix Stability)",
    whatItDoes:
      "Singular Value Decomposition se check karta hai ki mathematical transformation matrix mein koi singularity ya division-by-zero risk to nahi.",
    projectRole:
      "Agar condition number 10^5 se zyada ho to transformation distorted ho sakti hai. Humara score ~10^3 rehta hai jo rock-solid stability prove karta hai.",
    keywords: ["SVD Matrix Stability", "singularity", "10^5 se zyada", "rock-solid stability"]
  },
  grid_occupancy: {
    title: "Grid Occupancy (% Bins Filled)",
    whatItDoes:
      "8x8 grid ke kul 64 cells mein se kitne cells ke andar reliable inlier points maujood hain.",
    projectRole:
      "96.12% occupancy ensure karti hai ki moon ke kisi bhi chote se chote hisse mein geometric error na bacha ho.",
    keywords: ["64 cells", "reliable inlier points", "96.12% occupancy"]
  },
  photometric_ncc: {
    title: "Photometric NCC (Normalized Cross-Correlation)",
    whatItDoes:
      "Dono images ke pixel brightness patterns ka statistical correlation measure karta hai (-1 se +1 scale par).",
    projectRole:
      "Geometric alignment theek hone ke baad surface texture agreement confirm karta hai.",
    keywords: ["statistical correlation", "texture agreement"]
  },
  transformation_matrix: {
    title: "Transformation Matrix (Affine 2x3 Array)",
    whatItDoes:
      "Har pixel [x, y] ko naye coordinate [x', y'] par map karne ke coefficients [a11, a12, tx; a21, a22, ty].",
    projectRole:
      "ISRO cartographers isi matrix ko use karke raw lunar tiles ko seamless global mosaic mein stitch karte hain.",
    keywords: ["coefficients", "seamless global mosaic"]
  }
};
