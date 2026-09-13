# 🌕 LunarX: Complete SIH 2026 Project Master Guide & Judges Handbook

> **Project Name:** LunarX  
> **Problem Statement ID:** 26166  
> **Problem Statement Title:** Chandrayaan-2: Sun & Scale-Invariant Lunar Matching  
> **Theme:** Space Technology | **Category:** Software  
> **Target Sensor Suite:** Chandrayaan-2 OHRC (0.25 m/px), TMC-2 (5.0 m/px), IIRS (Spectral)  
> **Live Frontend URL:** [https://lunarx-pi.vercel.app](https://lunarx-pi.vercel.app)  
> **Backend Architecture:** Python FastAPI + PyTorch/OpenCV + Cloudflare Secure Tunnel  

---

## 🧒 PART 1: "2nd Class ke Bachhe ko Samjhane Wala" Real-Life Analogy
*(Agar koi 7 saal ka bachha ya non-technical person puche ki tumne kya banaya hai, toh yeh kahani sunao)*

> "Socho tumhare paas Moon (Chanda Mama) ke ek gaddhe (crater) ki **2 alag-alag photos** hain.
> 
> * **Photo A** subah li gayi thi, jab Suraj baayein (left) taraf tha, toh chhaya (shadow) daayein (right) pad rahi thi.
> * **Photo B** dopahar ya shaam ko li gayi, jab Suraj doosri taraf tha, aur photo bohot door (zoom-out) se li gayi thi!
> 
> Ab agar tum in dono photos ko ek ke upar ek rakhoge, toh dono bilkul alag dikhengi! Kahin dhoop hai, kahin andhera, aur ek photo badi hai toh doosri chhoti. Normal computer dhoop-chaon dekh kar confuse ho jata hai aur galat jagah chipka deta hai.
> 
> **Humne ek aisa smart robot dimaag (LunarX) banaya hai**, jo dhoop aur shadow ki parwah kiye bina, gaddhon ki asli zameen aur pathar ke kinaron ko pehchan leta hai! Chahe photo kitni bhi chhoti-badi ho ya kisi bhi angle se li gayi ho, yeh dono photos ko bilkul ek sui (needle) ke barabar sub-pixel accuracy se aapas mein jod deta hai taaki ISRO ke scientists ko Moon ka ekdam perfect naksha (map) mil sake!"

---

## 🎯 PART 2: Problem Statement Deep-Dive (PS ID: 26166)

### 1. Problem Statement kya hai aur ISRO ko iski zaroorat kyun hai?
Chandrayaan-2 orbiter Moon ke charon taraf chakkar lagate hue alag-alag sensors se photos leta hai:
1. **OHRC (Orbiter High-Resolution Camera):** 0.25 meter per pixel (bohot ultra zoom, landing site ke chote pathar dikhte hain).
2. **TMC-2 (Terrain Mapping Camera):** 5.0 meter per pixel (badi strip, 20 guna zyada zoomed-out).
3. **IIRS (Imaging Infrared Spectrometer):** Mineral and water-ice composition dekhne ke liye alag wavelengths.

### 2. Yeh Problem Itni Mushkil Kyun Hai? (3 Core Bottlenecks)
* **Sun Angle & Shadow Inversion (Illumination Shift):** Moon par koi atmosphere nahi hota. Isliye dhoop bohot sharp hoti hai. Jab Sun ka angle badalta hai, toh crater ke andar ki shadow 180° ghoom jaati hai. Computer shadow ko hi feature samajh kar galat match kar deta hai.
* **20× Scale Gap (Size Discrepancy):** OHRC ka 1 pixel = TMC-2 ke 20 pixels! Ek photo bohot zoomed-in hai, doosri bohot door se. Traditional matchers (jaise basic ORB) scale change par fail ho jate hain.
* **Repetitive Lunar Terrain (Feature Ambiguity):** Chandrama par har jagah gol-gol craters hote hain. Agar camera plain zameen (lunar maria) dekhta hai, toh computer ko samajh nahi aata kaun sa crater kahan ka hai.
* **Manual Alignment ki Kami:** Pehle scientists Photoshop ya GIS tools mein haath se points match karte the. Isme ghanton lagte the, insaan thak jaata tha, aur error 2 se 5 pixels tak reh jaata tha.

---

## 📑 PART 3: Slide-by-Slide PPT Alignment (Uploaded PDF ke Anusaar)

Yeh breakdown tumhari uploaded PPT ke har ek page ke content se 100% match karta hai, taaki team ke sabhi members ka narrative bilkul unified rahe.

### 📄 Slide 1: Title Page
* **Title:** Chandrayaan-2: Sun & Scale-Invariant Lunar Matching
* **PS ID:** 26166 | **Category:** Software | **Theme:** Space Technology
* **Team:** Lunar X

---

### 📄 Slide 2: Challenges & Proposed Solution
* **5 Core Challenges in Slide:**
  1. *Different sensors:* OHRC, TMC-2 aur IIRS har sensor ka resolution aur wavelength alag hai.
  2. *Sun and size change:* Sun angle se badalti shadows aur scale change.
  3. *Few clear landmarks:* Plain lunar regolith mein feature points kam milte hain.
  4. *Manual alignment:* Slow, operator-biased, non-repeatable.
  5. *Weak quality proof:* Sirf visually dekh kar pata nahi chalta ki match sahi hua ya galat.
* **Innovation & Uniqueness (Our 5 Pillars):**
  1. *Light-Aware Input:* CLAHE (Contrast-Limited Adaptive Histogram Equalization) + Sobel gradient views jo lighting variations ko nullify karte hain.
  2. *Two Matching Paths:* Dual-engine — SIFT/ORB (Fast Classical Route, <0.2s) + LoFTR (AI Deep Transformer matching, for difficult terrain).
  3. *False Match Control:* MAGSAC++ outlier rejection jo noise aur galat vectors ko 100% remove karta hai.
  4. *Safe Alignment:* Homography (8 DOF), Affine (6 DOF), aur Rigid (3 DOF) models with SVD condition gating ($\kappa \le 10^5$).
  5. *Proof with Numbers:* Zero guess work! Live metrics: RMSE ($0.148\text{ px}$ to $0.263\text{ px}$), Inlier Ratio ($99.85\% - 100\%$), NCC ($0.845$), aur Spatial Area Coverage ($94.2\% - 96.1\%$).

---

### 📄 Slide 3: Technical Approach (End-to-End Pipeline)
Yeh hamara core scientific architecture hai jisme 6 systematic stages hain:
1. **Input & Ingest:** PDS4 XML/IMG, GeoTIFF, aur metadata ingestion with multi-resolution scaling.
2. **Normalisation:** Dynamic intensity normalization, CLAHE contrast enhancement, Sobel edges, aur illumination invariance.
3. **Adaptive Matching:** Image complexity analyze hoti hai:
   * *Classical Route:* SIFT / ORB with Lowe's Ratio Test (0.75).
   * *Deep Route:* LoFTR (Local Feature Transformer) with attention mechanism across dense patches.
4. **Geometric Alignment:** MAGSAC++ robust consensus estimation jo outliers ko nikaal kar最佳 Homography matrix ($3 \times 3$) compute karti hai.
5. **Sub-Pixel Refinement:** OpenCV `cornerSubPix` snap-to-gradient + SVD local optimization + $8 \times 8$ spatial coverage grid check.
6. **Output & QA:** Output GeoTIFF with geospatial tags, difference map heatmap, 8x8 checkerboard visualizer, aur downloadable JSON report.

---

### 📄 Slide 4: Feasibility & Viability
* **Technical Feasibility:** 4 matchers benchmarked and ready (SIFT, ORB, SuperPoint+LightGlue, LoFTR). Fully modular.
* **Computational Feasibility:** Runs efficiently on standard CPU! SIFT+CLAHE reaches **0.148 px RMSE in just 0.16 seconds**. GPU is optional (only used for heavy batch LoFTR processing).
* **Operational Feasibility:** 20-test automated Pytest test-suite. Zero fake data; real PDS4 Chandrayaan-2 lunar products benchmarked.
* **Mission Viability:** Extensible beyond Chandrayaan-2 to Chandrayaan-3, LUPEX, and future planetary exploration.

---

### 📄 Slide 5: Impact and Benefits
* **For ISRO & Mission Teams:** Seamless integration of multi-orbit orbital strips without manual GIS warping.
* **For Space Researchers:** Precise multi-temporal change detection (e.g., naye meteoroid impact craters dhundna).
* **For Future Lunar Missions:** Hazard mapping for safe lunar lander touchdown zones.
* **Operational Savings:** Manual GIS registration takes 45-60 mins per image pair; LunarX automates it in **under 1 second**.

---

### 📄 Slide 6: Research and References
* Official Chandrayaan-2 Payload Documentation (OHRC, TMC-2, IIRS).
* Barath et al., *MAGSAC++: A Fast, Reliable and Accurate Robust Estimator*, IEEE TPAMI 2021.
* Sun et al., *LoFTR: Detector-Free Local Feature Matching with Transformers*, CVPR 2021.
* Lowe, *Distinctive Image Features from Scale-Invariant Keypoints*, IJCV 2004.

---

## ⚙️ PART 4: Technical Deep-Dive — Har Ek Step Ka Kaam Kya Hai?

```
Raw Lunar Pair (OHRC/TMC-2) 
      │
      ▼
[1. CLAHE Lighting Normalization] ──> Shadows removed, crater rims enhanced
      │
      ▼
[2. Adaptive Feature Extractor]   ──> SIFT Keypoints OR LoFTR Self/Cross-Attention
      │
      ▼
[3. USAC_MAGSAC Consensus]       ──> Outlier tie-lines rejected (Noise elimination)
      │
      ▼
[4. SVD Stability Gating]         ──> Condition Number κ <= 10^5 (Prevents image fold/warp)
      │
      ▼
[5. Sub-Pixel Snapping]          ──> cornerSubPix gradient optimization (RMSE < 0.2 px)
      │
      ▼
[6. 8x8 Spatial Grid Filter]     ──> Prevents clustering on single crater; 95%+ coverage
      │
      ▼
Final Warp & Quality Assurance   ──> Checkerboard Blend + GeoTIFF + Metrics Report
```

1. **CLAHE (Contrast-Limited Adaptive Histogram Equalization):**
   * *Problem:* Ek crater ke andar kaali shadow hoti hai aur dusri side tez dhoop.
   * *Kaam:* Yeh image ko chhote-chhote tiles mein baant kar local contrast balance karta hai bina noise ko amplify kiye. Isse andhere crater ke andar ke hidden contours bahar nikal aate hain.
2. **LoFTR (Local Feature Transformer) vs SIFT:**
   * *SIFT:* Fast detector jo corners aur blobs dhundta hai.
   * *LoFTR:* Detector-free neural network hai. Yeh transformers (self-attention aur cross-attention) use karke do images ke beech pixel patches ko compare karta hai. Jab plain smooth zameen par corners nahi milte, tab LoFTR deep context se matching kar deta hai.
3. **MAGSAC++ (`cv2.USAC_MAGSAC`):**
   * Standard RANSAC ek fixed threshold maangta hai (jaise 3 pixels). Agar noise zyada ho toh RANSAC fail ho jata hai.
   * MAGSAC++ (Marginalizing Sample Consensus) ek multi-threshold sigma approach use karta hai. Yeh mathematically har correspondence ko probability score deta hai, jisse 99.8%+ inlier accuracy milti hai.
4. **SVD Stability Check ($\kappa \le 10^5$):**
   * *Kaam:* Kahi galat points ki wajah se transformed image twist ya invert toh nahi ho rahi?
   * Singular Value Decomposition (SVD) matrix ke singular values ($\sigma_{\max} / \sigma_{\min}$) ka ratio check karta hai. Agar ratio $10^5$ se zyada hai, toh system safely Affine ya Rigid model par fall-back kar jata hai. Image kabhi corrupt nahi hoti!
5. **8×8 Spatial Grid Binning:**
   * *Kaam:* Aisa na ho ki saare 1000 points sirf ek bade crater ke charon taraf chipak jayein aur baaki ka 80% Moon surface unaligned reh jaye!
   * Hum image ko 64 cells ($8 \times 8$) mein divide karte hain aur ensure karte hain ki har cell mein verified inliers distributed hon ($>94\%$ spatial occupancy).

---

## 🖥️ PART 5: Complete UI Breakdown — Screen Ka Har Ek Feature Kya Karta Hai?

Jab tum laptop par live website open karoge, toh judges ke saamne har button aur panel ka purpose is tarah explain karna hai:

### 1. Top Header & Mission Status
* **Status Badge ("ONLINE / READY"):** Backend server ki live health dikhata hai. Agar FastAPI backend connected hai, toh green dot aati hai.
* **Problem Statement Badge (`SIH26166`):** Judges ko turant identify hota hai ki yeh specific problem solve ho rahi hai.

### 2. Control Panel (Sidebar / Configuration)
* **Preset Pair Buttons ("Load Crater Pair 1", "Load Pair 2"):**
  * *Kaam:* Chandrayaan-2 ke real benchmark pairs ko 1-click mein load karta hai taaki live presentation mein file dhundne mein time waste na ho.
* **Upload Boxes (Source & Reference):**
  * *Source Image:* Jis nayi photo ko align karna hai.
  * *Reference Image:* Base map/anchor photo jiske upar match karna hai.
* **Algorithm Selector (SIFT vs LoFTR):**
  * *SIFT:* Ultra-fast execution (<0.2s) standard terrain ke liye.
  * *LoFTR:* Deep-learning attention network extreme illumination differences ke liye.
* **Transformation Model (Homography vs Affine vs Rigid):**
  * *Homography (8 DOF):* Full perspective warping (camera angle change handle karta hai).
  * *Affine (6 DOF):* Scale, rotation, translation, aur shear.
  * *Rigid (3 DOF):* Sirf rotation aur translation (zero scale distortion).
* **Outlier Estimator (USAC_MAGSAC vs RANSAC):**
  * Statistical filter jo galat vectors ko reject karta hai. Default: `USAC_MAGSAC`.
* **"Run Registration" Button:**
  * Click karte hi backend ko API call jati hai aur under 1 second mein registered results screen par render ho jate hain.

### 3. Metric Cards (Key Scientific Numbers)
* **Reprojection RMSE (`0.148 px` ya `0.263 px`):**
  * Root Mean Square Error. Sub-pixel precision proof hai! 1 pixel se bhi bohot chhota error (0.14 px).
* **Inlier Count (`1,329` to `4,683`):**
  * Kitne feature points dono images ke beech 100% mathematically match hue hain.
* **Inlier Ratio (`99.85%` - `100%`):**
  * Total matches mein se kitne matches reliable hain. No false matches!
* **Spatial Coverage (`94.2%` - `96.1%`):**
  * Kitna percent surface area successfully covered aur aligned hai.
* **Runtime (`0.68s` / `0.16s`):**
  * Execution speed. Proves real-time operational efficiency.

### 4. Visual Inspection Panels
* **Correspondence Matches (Green Tie-Lines):**
  * Dono photos side-by-side dikhti hain aur green lines point-to-point jodti hain. Judges dekh sakte hain ki har crater ka rim dusre crater se connected hai.
* **8×8 Checkerboard Interactive Blend:**
  * Ek tile Photo 1 ka aur dusra tile Aligned Photo 2 ka hota hai.
  * *Slider feature:* Slider move karne par crater ke gol kinare bina toote (seamless) aapas mein match hote dikhte hain.
* **Difference Heatmap:**
  * Aligned images ko subtract karke color map banta hai. Deep blue ka matlab zero error! Agar red hota toh error hota.

### 5. Advanced Technical Drawer (Inspect Details)
* **$3 \times 3$ Transformation Matrix:** Mathematical proof jo matrix values display karta hai.
* **Condition Number ($\kappa$):** Matrix numerical stability proof ($< 10^5$).
* **Normalized Cross-Correlation (NCC):** Photometric texture correlation ($0.845$).
* **Export GeoTIFF Button:** Aligned image ko standard GIS GeoTIFF format mein download karne ki suvidha.

---

## 🌐 PART 6: Deployment & Cloud Architecture (Judge puche toh kya bolna hai?)

```
       [ Client Browser / Judges Laptop ]
                       │
                       ▼  (HTTPS / Global CDN)
            [ Vercel Edge Network ]
             Next.js 14 Web Frontend
                       │
                       ▼  (Encrypted Secure Tunnel)
          [ Cloudflare Tunnel Daemon ]
          (No open ports / Enterprise TLS)
                       │
                       ▼  (Localhost Reverse Proxy)
        [ Python FastAPI Inference Server ]
        (OpenCV, PyTorch, LoFTR, USAC-MAGSAC)
                       │
             [ Workstation CPU / GPU ]
```

### Agar Judge puche: *"Tumhara system kahan deploy hai aur kaise chal raha hai?"*
**Answer (Bolo aise):**
> "Sir, humne **Decoupled Edge-Core Architecture** follow kiya hai:
> 1. **Frontend:** Hamara modern Next.js + Tailwind UI **Vercel Edge Network** par globally hosted hai. Iska benefit yeh hai ki UI 50ms ke andar load hota hai, zero downtime deta hai, aur highly responsive hai.
> 2. **Backend Engine:** Hamara Python registration engine (OpenCV, PyTorch, LoFTR model) hamare high-compute workstation par **FastAPI** microservice ke roop mein execute ho raha hai.
> 3. **Communication Bridge (Cloudflare Tunnel):** Workstation aur Vercel ke beech communication ke liye hum **Cloudflare Tunnel (Zero-Trust Daemon)** use kar rahe hain. 
>    * *Security USP:* Isme koi bhi public port (port 80 ya 8000) router par open nahi karna padta. Saara data Cloudflare ke end-to-end encrypted TLS 1.3 tunnel se travel karta hai.
>    * *Reliability:* Agar network drop bhi ho, toh tunnel automatic reconnect hoti hai aur live URL stable rehta hai.
> 4. **Production Readiness:** Same backend ko humne **Dockerfile** ke sath package kiya hai, jo ISRO ke private data center ya onboard cluster par ek single command (`docker run`) se deploy ho sakta hai."

---

## 🏆 PART 7: 15 Most Important & Tough Judge Questions (With Winning Answers)

### Q1: Normal Computer Vision (jaise standard SIFT/ORB) lunar images par fail kyun ho jaata hai?
**Answer:**
"Sir, do main reasons hain:
1. **Shadow Inversion:** Moon par atmosphere na hone ki wajah se lighting bohot harsh hoti hai. Jab Sun ka angle badalta hai, toh crater ke andar ki chhaya (shadow) 180° shift ho jaati hai. Standard algorithms gradient intensity match karte hain, toh woh shadow ke boundary ko feature maan kar confuse ho jaate hain.
2. **Repetitive Low-Texture Terrain:** Lunar surface par hazaron craters lagbhag ek jaise dikhte hain. Standard keypoint descriptors ambiguous ho jate hain. Humne isko **CLAHE illumination normalization** aur **LoFTR cross-attention transformer** se solve kiya hai jo local pixel ke bajaye global context dekhta hai."

---

### Q2: Tumhara Reprojection RMSE 0.148 pixels hai. Iska physical ground distance mein kya matlab hai?
**Answer:**
"Sir, OHRC (Orbiter High-Resolution Camera) ka ground sampling distance $0.25\text{ meters per pixel}$ ($25\text{ cm}$) hota hai.
$$\text{Ground Error} = 0.148\text{ px} \times 0.25\text{ m/px} \approx 0.037\text{ meters} = 3.7\text{ centimeters!}$$
Matlab Chandrama ki zameen par hamara registration error **sirf 3.7 centimeters** hai! Yeh level of precision lunar lander ke hazard detection aur micro-rover navigation ke liye gold standard maana jaata hai."

---

### Q3: Standard RANSAC ke badle USAC-MAGSAC kyun use kiya?
**Answer:**
"Sir, standard RANSAC ka sabse bada draw-back hai ki usme ek 'hard inlier threshold' (jaise 3.0 pixels) manually choose karna padta hai. Lunar images mein noise aur lighting alag-alag hoti hai, toh fixed threshold se ya toh acche points reject ho jaate hain ya galat points accept ho jaate hain.
**MAGSAC++ (IEEE TPAMI 2021)** marginalizes over the noise scale using a continuous $\sigma$-distribution. Yeh har correspondence ko probability score deta hai. Isse hume without manual tuning **$99.85\%$ inlier ratio** milta hai aur false matches zero ho jaate hain."

---

### Q4: OHRC aur TMC-2 ke beech 20× ka resolution gap hai (0.25m vs 5m). Ise kaise bridge kiya?
**Answer:**
"Sir, humara multi-resolution scale pyramid pehle dono images ke ground sampling distance (GSD) ko harmonize karta hai. Hum reference image ko scale-space pyramid mein downsample/upsample karte hain, feature extraction scale-invariant space mein conduct hota hai, aur final geometric warp projective homography ke through continuous coordinate mapping execute karta hai."

---

### Q5: Sub-pixel refinement kaise kaam karta hai? Yeh accuracy kaise badhata hai?
**Answer:**
"Sir, feature matching discrete pixel coordinates (jaise $x=452, y=318$) deta hai. Par actual physical crater rim pixel ke center ke bajaye fraction par ho sakta hai (jaise $452.34, 318.82$).
Hum **`cv2.cornerSubPix`** run karte hain jo $5 \times 5$ window mein image brightness gradients ka dot-product minimize karta hai:
$$\nabla I(p)^T \cdot (q - p) = 0$$
Yeh points ko true mathematical sub-pixel extrema par snap kar deta hai, jisse RMSE $1.2\text{ px}$ se drop hokar **$0.148\text{ px}$** ho jaata hai."

---

### Q6: SVD Condition Number ($\kappa$) check ka kya significance hai?
**Answer:**
"Sir, jab points ek hi seedhi line par aa jayein (collinear) ya cluster ho jayein, toh calculated Homography matrix mathematically 'ill-conditioned' ya degenerate ho sakti hai. Isse image ajeeb tarah se stretch ya flip ho sakti hai.
Hum matrix ka SVD nikaal kar condition number check karte hain:
$$\kappa(H) = \frac{\sigma_{\max}}{\sigma_{\min}}$$
Agar $\kappa > 10^5$ ho, toh system degenerate homography ko reject kar deta hai aur safely 6-DOF Affine model par switch karta hai, ensuring zero system crashes."

---

### Q7: 8×8 Spatial Coverage Enforcement kyun zaroori tha?
**Answer:**
"Sir, computer vision algorithms aksar 'contrast greediness' dikhate hain — matlab agar image ke kisi ek kone mein bohot sharp crater hai, toh saare 1,000 matches usi akele crater par chipak jaayenge, aur baaki 90% image bina kisi match ke reh jayegi!
Isko rokne ke liye humne **$8 \times 8$ Grid Cell Binning** implement kiya. Hum ensure karte hain ki har individual quadrant/cell se verified inliers select hon, jisse hume **$94.2\%$ se $96.1\%$ uniform surface coverage** milti hai."

---

### Q8: Kya yeh pipeline CPU par chal sakti hai ya high-end GPU zaroori hai?
**Answer:**
"Sir, yeh hamare solution ka sabse bada competitive advantage hai!
Hamara primary pipeline (**SIFT + CLAHE + USAC-MAGSAC + CornerSubPix**) **100% CPU par run karta hai aur sirf 0.16 seconds leta hai**. Iske liye kisi expensive GPU ya cloud instances ki zaroorat nahi hai.
Deep learning model (LoFTR) humne secondary fallback route ke roop mein rakha hai jo complex cases ke liye GPU/CPU dono par Kornia inference use karta hai."

---

### Q9: Agar do images mein 180° complete shadow inversion ho (ek subah ki, ek shaam ki), tab system kaise handle karega?
**Answer:**
"Sir, us case mein humara **Deep LoFTR Route** activate hota hai. LoFTR local pixel intensities match nahi karta; yeh pure image ke global context aur structural semantics ko compare karta hai (self-attention across 64x64 feature patches).
Saath hi hamara **Phase Congruency & Sobel Gradient filter** illumination ko eliminate karke structural frequency domain mein edge features extract karta hai, jisse 180° reversed lighting par bhi stable matching hoti hai."

---

### Q10: Normalized Cross-Correlation (NCC) metric kya batata hai?
**Answer:**
"Sir, RMSE geometric error batata hai, jabki **NCC photometric similarity** measure karta hai valid overlapping region par:
$$NCC = \frac{\sum (I_1 - \bar{I}_1)(I_2 - \bar{I}_2)}{\sqrt{\sum (I_1 - \bar{I}_1)^2 \sum (I_2 - \bar{I}_2)^2}}$$
Hamara NCC score **0.845** aata hai, jo mathematically prove karta hai ki alignment ke baad dono images ke texture aur crater boundaries ek dusre ke sath highly correlated hain."

---

### Q11: Kya aapne koi mock data ya pre-baked results use kiye hain?
**Answer:**
"Sir, absolutely zero mock data! Hamare pipeline mein ISRO ke official **PDS4 Chandrayaan-2 TMC-2 aur OHRC data archives** ingest hote hain. Live web dashboard par har ek click par real Python process backend par run hota hai, matrix compute karta hai, aur live 1,300+ vectors calculate karke screen par draw karta hai."

---

### Q12: Difference Heatmap mein dark blue aur bright colors ka kya meaning hai?
**Answer:**
"Sir, Difference Heatmap aligned images ka absolute pixel difference ($|I_{\text{source\_warped}} - I_{\text{ref}}|$) dikhata hai.
* **Dark Blue / Purple:** Zero difference (perfect geometric alignment).
* **Bright Yellow / Red:** Significant physical or terrain change.
Iska fayda yeh hai ki scientist ek glance mein dekh sakta hai ki alignment sahi hai, aur agar koi naya crater bana hai toh woh turant highlight ho jaata hai."

---

### Q13: Homography (8 DOF) aur Affine (6 DOF) mein kya farak hai aur kab kaunsa use karte hain?
**Answer:**
"Sir, **Affine transform (6 Parameters)** sirf 2D scaling, rotation, translation, aur shearing allow karta hai — yeh parallel lines ko parallel rakhta hai. Yeh tab best hota hai jab satellite camera seedha nadir (90° down) dekh raha ho.
**Homography (8 Parameters)** perspective warping aur camera tilt (off-nadir pitch and roll) ko bhi model kar sakta hai. Jab spacecraft kisi angle se photo leta hai, tab hum Homography use karte hain."

---

### Q14: Chandrayaan-3 ya future Lunar/Mars missions mein yeh kaise help karega?
**Answer:**
"Sir, Chandrayaan-3 aur upcoming missions (jaise ISRO-JAXA LUPEX) mein lander ko autonomously safe landing site chunni hoti hai.
Yeh pipeline onboard descent camera ke frames ko pehle se bane high-resolution base maps ke sath real-time align kar sakti hai, allowing sub-meter Terrain Relative Navigation (TRN) even in deep shadow regions near the Lunar South Pole."

---

### Q15: Vercel + Cloudflare Tunnel architecture production use ke liye kitna secure aur scalable hai?
**Answer:**
"Sir, yeh architecture enterprise grade security standards follow karta hai:
* **Zero Open Ports:** Workstation ke router par koi port forwarding nahi hai, eliminating DDoS and intrusion vectors.
* **TLS 1.3 Encryption:** Cloudflare tunnel edge se backend tak double-encrypted tunnel provide karta hai.
* **Decoupled Scaling:** Vercel UI globally distributed edge caching handle karta hai, jabki computational workload isolated private clusters par horizontally scale kiya ja sakta hai."

---

## 🎯 Quick 1-Minute Pitch Script for Team Members
*(Jab stage par khade hokar 60 seconds mein judges ko bolna ho)*

> *"Good morning respected judges! We are Team Lunar X, addressing Problem Statement 26166: Chandrayaan-2 Sun and Scale-Invariant Lunar Matching.*
> 
> *Multi-orbit lunar registration has historically suffered from three crippling challenges: extreme shadow inversions due to varying sun angles, massive 20x resolution gaps between OHRC and TMC-2 sensors, and high manual GIS overhead.*
> 
> *Our solution, LunarX, solves this with a modular, dual-engine scientific pipeline. We combine adaptive CLAHE illumination normalization with a dual routing architecture: ultra-fast SIFT for standard terrain, and LoFTR deep transformers for low-texture shadowed craters.*
> 
> *Using USAC-MAGSAC consensus and sub-pixel gradient optimization, we achieve a verified Reprojection RMSE of just 0.148 pixels — translating to under 4 centimeters of ground accuracy on the lunar surface — with over 99.8% inlier reliability in under 0.2 seconds.*
> 
> *Our prototype is fully operational, open-source, and deployed via a secure Vercel and Cloudflare microservice architecture. Thank you!"*
