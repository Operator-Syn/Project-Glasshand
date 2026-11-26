# Talking points — EDA deck

Ten slides. About 12 minutes.

## The measure

Define this once, at slide 1. Then use the same words on every slide.

**Target area** = the area of the target box, as a percentage of the screen area.

Do not say "the target is small". Say "the target area is small". The target is a box. The area is the measurement.

## How to speak

- Speak in the present tense.
- Say the number first.
- Then say what the number means.
- Then stop.
- Do not read the slide.
- Keep each sentence below 20 words.
- Put one idea in each sentence.

---

## Slide 1 — Opening (60 s)

**Point:** The target areas are small.

- Define the measure. Say: "The target area is the area of the target box, as a percentage of the screen area."
- Give the median. Say: "The median target area is 0.0382% of the screen."
- Give the scope. Say: "This report examines 1,020 requests from 17 Windows applications."
- Give the three questions. Say: "What is in the table? Can we trust the table? What do the target areas show?"
- Give the counts. Say: "The table has 1,020 requests, 17 applications and 6 industry groups." Then: "It has 1,006 distinct contents and 14 duplicate pairs."

**Do not say** that the corpus is representative of all desktop work. It is one benchmark.

---

## Slide 2 — What one row is (80 s)

**Point:** One row is one request.

- Define the row. Say: "A row has a screenshot, an instruction and the box around the target."
- List the missing fields. Say: "The release has no outcome label, no confidence score and no timestamp."
- State the limit. Say: "This report describes the task. It does not describe a model result."
- Show the group sizes. Say: "Creative has 297 requests, or 29.1%." Then: "Dev has 45 requests. All 45 come from one application."
- Give the result. Say: "Do not average by group. The groups have very different sizes."
- Explain the duplicates. Say: "Fourteen pairs of files are byte-identical." Then: "Each pair has two different instructions. Both requests stay. They are not independent."

**Do not say** that the duplicate pairs are errors. They are real requests. They share one image.

---

## Slide 3 — Verification (60 s)

**Point:** The merged table agrees with the source files.

- Give the method. Say: "The merge compares 14 fields against 17 raw files."
- Give the result. Say: "All 1,020 rows agree. No row is missing. No field is empty."
- Give the image check. Say: "Every image decodes as RGB at the size in the table."

**Do not say** that the data is clean. Say that the merge is exact. The repairs come next.

---

## Slide 4 — Repairs (90 s)

**Point:** Three repairs touch 102 rows. No row is lost.

- Give the count first. Say: "Three repairs touch 102 rows. All 1,020 rows stay."
- Repair one. Say: "The release marks 93 MATLAB captures as macOS." Then: "The screenshots show a Windows taskbar and a D: path. We change the label to Windows."
- Repair two. Say: "Eight instructions have extra spaces. We remove the spaces before we count characters."
- Repair three. Say: "One box starts at y equal to minus one, above the screen edge. We set the value to zero."
- State the rule. Say: "The source file does not change. The clean table adds 15 derived columns."

**Do not say** that we corrected the dataset. Say that we recorded three repairs.

---

## Slide 5 — Target area distribution (90 s)

**Point:** Target area is heavily skewed. Use the median.

- Give the median. Say: "The median target area is 0.0382% of the screen."
- Give the plain meaning. Say: "Half of the requests have a target area below this value."
- Give the range. Say: "Target area runs from 0.0021% to 4.73% of the screen." Then: "That range is more than three orders of magnitude."
- Give the skew. Say: "The skew is 20.3."
- Give the mean for contrast. Say: "The mean target area is 0.0653% of the screen." Then: "66.5% of the requests are below the mean."
- Give the spread. Say: "The interquartile range is 0.014% to 0.081% of the screen."
- Give the rule. Say: "Every comparison in this report uses the median and a rank test."

**Do not say** the average target area as if it were typical. Two of every three requests are below it.

---

## Slide 6 — Icons and text (80 s)

**Point:** Icon areas are much smaller than text areas.

- Give both medians. Say: "The median icon area is 0.0144% of the screen." Then: "The median text area is 0.0684% of the screen."
- Give the ratio. Say: "The median icon area is 4.7 times smaller than the median text area."
- Give the counts. Say: "The corpus has 622 text requests and 398 icon requests."
- Give the check. Say: "The gap is present inside almost every application that has both types."
- Give the rule. Say: "Report the two types apart. One value for both is misleading."

**Do not say** that icons fail because they are small. This slide shows target area. It does not test success.

---

## Slide 7 — Applications (80 s)

**Point:** Target area varies across applications.

- Give the spread. Say: "The median target area varies by 11.8 times across applications."
- Give the low value. Say: "Origin has the smallest median, at 0.0067% of the screen."
- Give the high value. Say: "MATLAB has the largest median, at 0.0783% of the screen."
- Give the variance split. Say: "16.9% of the variance in log target area is between applications." Then: "83.1% of the variance is within applications."
- Give the cause. Say: "Part of the spread is interface style. Part is the mix of target types." Then: "Stata has an icon share of 84%. EViews has 14%."
- Give the rule. Say: "Keep application in every model."

**Do not say** that the application causes the size. The mix of target types inside the application also matters.

---

## Slide 8 — Resolution (80 s)

**Point:** This corpus cannot separate resolution from application.

- Give the structure. Say: "The corpus has seven resolutions."
- Give the confound. Say: "15 of the 17 applications have one resolution only."
- Give the thin cell. Say: "19 requests use 1920 by 1080."
- State the limit. Say: "Resolution and application change together here. We cannot measure a resolution effect."
- Give the rule. Say: "Do not use resolution as a feature. Report it as a limitation."

**Do not say** that resolution has no effect. Say that this corpus cannot measure the effect.

---

## Slide 9 — Instruction length (80 s)

**Point:** Instruction length has no association with target area.

- Give the median. Say: "The median instruction has 4 words and 20 characters."
- Give the short ones. Say: "78 instructions have one word only."
- Give the position words. Say: "25 instructions name a position. That is 2.5%."
- Give the association. Say: "The rank correlation between instruction length and target area is minus 0.023."
- Give the rule. Say: "Do not use instruction length as a proxy for target area."

**Do not say** that instruction text is useless. Length has no signal. The words can still help a matcher. This deck does not test that.

---

## Slide 10 — Decisions (90 s)

**Point:** These measurements set four rules for the analysis that follows.

- Rule one. Say: "Use the median, not the mean. The skew is 20.3."
- Rule two. Say: "Report icons and text apart. The median areas differ by 4.7 times."
- Rule three. Say: "Keep application in every model. 16.9% of the variance is between applications."
- Rule four. Say: "Do not use resolution as a feature. 15 of 17 applications have one resolution."
- State the boundary. Say: "This deck reports the corpus. It does not report grounding accuracy."
- Name the next step. Say: "The grounding results come next. They use the same 1,020 requests."
- Cite the source. Say: "The data is ScreenSpot-Pro, by Li and others, 2025, under the MIT licence."

---

## If someone asks

- **Why keep the duplicate pairs?** They are real requests. They share one image. We keep them and we treat them as dependent. Validation is grouped.
- **Why change the 93 macOS labels?** The label is wrong. The screenshots show Windows. We record the repair and keep the rows.
- **Why the median?** The skew is 20.3. Two of every three requests are below the mean.
- **Can you claim a resolution effect?** No. 15 of 17 applications have one resolution only.
- **Is 2.5% position words a problem?** No. The instructions rarely give the answer. The corpus does not test the matcher on easy targets.
- **What does this prove about the model?** Nothing yet. This deck measures the task. The next deck measures one baseline on the same requests.

## Delivery notes

- Pause after each number. Give the audience time to read it.
- If you run short, cut slides 3 and 7. Keep 1, 5, 6, 8 and 10.
- Do not defend a number that is not on the slide.
