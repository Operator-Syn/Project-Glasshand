# Talking points — EDA deck

Ten slides. About 12 minutes. Each slide has one point to make, then the number that supports it.

## How to speak

- Use the present tense. Say "the median is", not "the median was found to be".
- Say the number first. Then say what the number means. Then stop.
- Do not read the slide. The slide shows the evidence. You give the meaning.
- Keep each sentence short. One idea in each sentence.
- Do not claim more than the table shows. Each slide has a "Do not say" line. Obey it.

---

## Slide 1 — Opening (60 s)

**Point:** The targets in this corpus are very small.

- Start with the headline. "The median target covers 0.0382% of the screen."
- Give the scope. "This report covers the Windows subset of ScreenSpot-Pro. It has 1,020 requests from 17 applications."
- Give the three questions. "What is in the table? Can we trust the table? What do the sizes mean?"
- Name the evidence. "The counts come from the released annotations and from the screenshots."
- Read the five counts in order. 1,020 requests. 17 applications. 6 industry groups. 1,006 distinct contents. 14 duplicate pairs.

**Do not say** that the corpus is representative of all desktop work. It is one benchmark.

---

## Slide 2 — What one row is (80 s)

**Point:** One row is one request, not one screen and not one element.

- Define the row. "A row is one request. It has a screenshot, an instruction, and the box around the target."
- Say what is absent. "The release has no outcome label, no confidence score, and no timestamp. This report describes the task, not a model's result."
- Show the group imbalance. "Creative holds 297 requests, or 29.1%. Dev holds 45 requests, and they all come from one application."
- Draw the consequence. "An average by group mixes very different sample sizes. Do not average by group."
- Explain the duplicates. "Fourteen pairs of files are byte-identical. Each pair carries two different instructions. Both requests stay. They are not independent."

**Do not say** that the duplicates are errors. They are real requests that share one image.

---

## Slide 3 — Verification (60 s)

**Point:** The merged table matches the source files.

- State the method. "The merge compares 14 fields against 17 raw files."
- Give the result. "All 1,020 rows agree. No row is missing on either side. No field is empty."
- Give the image check. "Every image decodes as RGB at the size that the table records."

**Do not say** that the data is clean. Say that the merge is exact. Cleaning comes next.

---

## Slide 4 — Repairs (90 s)

**Point:** Three repairs touch 102 rows. We drop no row.

- Say the count first. "Three repairs. 102 rows. No row is lost."
- Repair one. "The release marks 93 MATLAB captures as macOS. The screenshots show a Windows taskbar and a D: path. We change the label to Windows."
- Repair two. "Eight instructions have extra spaces at the start, at the end, or inside. We strip and collapse the spaces before we count characters."
- Repair three. "One box starts above the top edge of the screen, at y equal to minus one. We clamp the value to zero."
- State the rule. "The source file does not change. The cleaned table keeps all rows and adds 15 derived columns."

**Do not say** that we corrected the dataset. Say that we recorded three local repairs.

---

## Slide 5 — Target size (90 s)

**Point:** The distribution is heavily skewed, so the median carries the finding.

- Give the centre. "Half of the targets cover less than 0.0382% of the screen."
- Give the range. "Areas run from 0.0021% to 4.73%. That is more than three orders of magnitude."
- Give the shape. "Skew is 20.3. The mean is 0.0653%, and it describes a target that few requests contain."
- Give the spread. "The interquartile range is 0.014% to 0.081%."
- State the consequence. "Every comparison in this report uses the median and a rank test."

**Do not say** the average target size. The mean does not describe this table.

---

## Slide 6 — Icons and text (80 s)

**Point:** An icon target is 4.7 times smaller than a text target.

- Give both medians. "The median icon covers 0.0144%. The median text target covers 0.0684%."
- Give the ratio. "An icon is 4.7 times smaller."
- Give the counts. "The corpus has 622 text requests and 398 icon requests."
- State the check. "The gap holds inside almost every application that contains both types."
- Draw the consequence. "Report the two types apart. One coefficient across both is misleading."

**Do not say** that icons are harder because they are small. This slide shows size. It does not test success.

---

## Slide 7 — Applications (80 s)

**Point:** Target size changes by 11.8 times across applications.

- Give the spread. "The median size varies 11.8 times across applications."
- Give the extremes. "Origin is the smallest at 0.0067%. MATLAB is the largest at 0.0783%."
- Give the decomposition. "16.9% of the variance in log target area sits between applications. 83.1% sits inside them."
- Name the cause. "Part of the spread is interface style. Part is the target mix. Stata has an icon share of 84%. EViews has 14%."
- Draw the consequence. "Keep application in every model. It explains a real share of the variation."

**Do not say** that the application causes the size. The mix of targets inside the application also matters.

---

## Slide 8 — Resolution (80 s)

**Point:** This corpus cannot separate resolution from application.

- Give the structure. "There are seven resolutions. 15 of the 17 applications appear at only one resolution."
- Give the thin cell. "Only 19 requests use 1920 by 1080."
- Give the correlation. "The pooled rank correlation is minus 0.088."
- Draw the consequence. "Resolution is locked to application here. We cannot estimate a resolution effect."
- State the rule. "Do not use resolution as a feature. Report it as a limitation."

**Do not say** that resolution has no effect. Say that this corpus cannot measure the effect.

---

## Slide 9 — Instruction length (80 s)

**Point:** Instruction length does not predict target size.

- Give the centre. "The median instruction is 4 words and 20 characters."
- Give the extremes. "78 requests use one word. 25 requests name a position, which is 2.5%."
- Give the association. "The rank correlation with target area is minus 0.023."
- Draw the consequence. "Instruction length carries no signal about target size in this corpus. Do not use it as a size proxy."

**Do not say** that instruction text is useless. Length carries no signal. The words may still help a matcher. This deck does not test that.

---

## Slide 10 — Decisions (90 s)

**Point:** The measurements set four rules for the analysis that follows.

- Rule one. "Use the median, not the mean. The distribution is skewed at 20.3."
- Rule two. "Report icons and text apart. They differ by 4.7 times."
- Rule three. "Keep application in every model. 16.9% of the variance is between applications."
- Rule four. "Do not use resolution as a feature. 15 of 17 applications use one resolution."
- Close on the boundary. "This deck reports the corpus. It does not report grounding accuracy. The grounding results come next, and they use the same requests."
- Cite the source. "ScreenSpot-Pro, Li and others, 2025. Data under the MIT licence."

---

## If someone asks

- **"Why keep the duplicate pairs?"** They are real requests. They share one image. We keep them and we treat them as dependent, so validation is grouped.
- **"Why change the 93 macOS labels?"** The label is wrong. The screenshots show Windows. We record the repair and keep the rows.
- **"Why the median?"** The skew is 20.3. The mean describes a target that few requests contain.
- **"Can you claim a resolution effect?"** No. 15 of 17 applications use one resolution. The two variables move together.
- **"Is 2.5% position words a problem?"** No. It means the instructions rarely give away the answer. The corpus does not spoon-feed the matcher.
- **"What does this prove about the model?"** Nothing yet. This deck measures the task. The next deck measures the baseline on the same requests.

## Delivery notes

- Pause after each number. Let the slide do the work.
- If you run out of time, cut slides 3 and 7. Keep 1, 5, 6, 8, and 10.
- Never defend a number you cannot point to on the slide.
