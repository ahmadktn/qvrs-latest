/**
 * =========================================================================================
 * BUK-SIWES QOVRS: Student Requirements Elicitation Questionnaire Generator
 * Department of Software Engineering, Bayero University Kano (BUK)
 * Project: SIWES Quality, Organization Vetting and Rating System
 * =========================================================================================
 * 
 * DESCRIPTION:
 * Concise, student-focused Google Apps Script that creates a Google Form specifically
 * targeting undergraduate students (SIWES candidates & returnees).
 * 
 * Based directly on BUK-SIWES QOVRS Chapter 3:
 * - Table 3.1: Student Need ("Difficulty in identifying suitable organizations; limited information about organization quality")
 * - Documented problems: Poor training quality, menial tasks (photocopying, errands, idle waiting), zero organizational accountability
 * - Proposed system features: Pre-placement vetting, approved directory, supervisor ratings, and blacklisting
 * 
 * HOW TO USE:
 * 1. Open https://script.google.com
 * 2. Paste this code into Code.gs
 * 3. Select 'createStudentSiwesQuestionnaire' and click 'Run'
 * 4. Check the Execution Log (View > Execution log) for the Edit URL and Response URL
 * =========================================================================================
 */

function createStudentSiwesQuestionnaire() {
  const formTitle = "BUK-SIWES QOVRS: Student Requirements Survey";
  const formDescription = 
    "Department of Software Engineering, Bayero University Kano (BUK)\n" +
    "Research Project: SIWES Quality, Organization Vetting and Rating System (BUK-SIWES QOVRS)\n\n" +
    "Dear Student,\n" +
    "This brief survey gathers your input to help design BUK-SIWES QOVRS—a system to ensure SIWES placements offer " +
    "genuine, curriculum-relevant software engineering training rather than menial tasks (e.g., photocopying, running errands, or idle waiting). " +
    "Your responses will directly shape the features of the new platform. Takes approximately 2–3 minutes.";

  // 1. Create Form
  const form = FormApp.create(formTitle);
  form.setDescription(formDescription);
  form.setConfirmationMessage("Thank you! Your response has been recorded and will inform the design of BUK-SIWES QOVRS.");
  form.setAllowResponseEdits(false);
  form.setAcceptingResponses(true);
  form.setShowLinkToRespondAgain(false);

  // =======================================================================================
  // PART 1: STUDENT PROFILE
  // =======================================================================================
  
  // Academic Level / SIWES Status
  form.addMultipleChoiceItem()
    .setTitle("1. What is your current academic level / SIWES status?")
    .setChoiceValues([
      "300 Level (Preparing for SIWES)",
      "400 Level (Currently on SIWES or just returned)",
      "500 Level / Final Year (Completed SIWES)"
    ])
    .setRequired(true);

  // Department / Course of Study
  form.addMultipleChoiceItem()
    .setTitle("2. Course of Study")
    .setChoiceValues([
      "B.Sc. Software Engineering",
      "B.Sc. Computer Science",
      "B.Sc. Information Technology",
      "Other Computing / Engineering programme"
    ])
    .setRequired(true);

  // =======================================================================================
  // PART 2: PLACEMENT CHALLENGES & TRAINING QUALITY (Problems Being Solved)
  // =======================================================================================

  // Finding suitable placement
  form.addMultipleChoiceItem()
    .setTitle("3. How challenging was it (or is it) to find an organization offering genuine, curriculum-relevant software engineering work?")
    .setChoiceValues([
      "Very Difficult - Most organizations have no relevant IT roles",
      "Moderately Difficult - Required lots of trial and error",
      "Neutral / Average",
      "Easy - Found a suitable technical placement without difficulty"
    ])
    .setRequired(true);

  // Training quality issues experienced or observed
  form.addCheckboxItem()
    .setTitle("4. Which of these issues have you experienced or observed during SIWES? (Select all that apply)")
    .setChoiceValues([
      "Assigned menial/unrelated tasks (e.g., photocopying, typing casual letters, running errands)",
      "Idle waiting with little or no technical work or supervision",
      "Mismatch between the company's core work and your university curriculum",
      "No qualified technical mentor/supervisor to guide practical learning",
      "None - Placements provided high-quality engineering training"
    ])
    .showOtherOption(true)
    .setRequired(true);

  // =======================================================================================
  // PART 3: PROPOSED SYSTEM FEATURES & REQUIREMENTS
  // =======================================================================================

  // Approved Directory
  form.addScaleItem()
    .setTitle("5. How helpful would an 'Approved Organization Directory' be, where you can browse vetted organizations before applying?")
    .setBounds(1, 5)
    .setLabels("Not Helpful", "Extremely Helpful")
    .setRequired(true);

  // Quality Ratings & Track Record
  form.addScaleItem()
    .setTitle("6. How important is it for students to see past supervisor ratings (1–5 stars) and training track records of organizations in the directory?")
    .setBounds(1, 5)
    .setLabels("Not Important", "Very Important")
    .setRequired(true);

  // Blacklisting / Pre-vetting gate
  form.addMultipleChoiceItem()
    .setTitle("7. Should the system block students from applying to organizations that failed departmental vetting or were blacklisted for poor training?")
    .setChoiceValues([
      "Yes - Strongly agree (Protects students from wasting their SIWES period)",
      "Neutral / Undecided",
      "No - Students should be free to place anywhere they find an offer"
    ])
    .setRequired(true);

  // Desired Portal Features
  form.addCheckboxItem()
    .setTitle("8. Which portal features would you use the most as a student? (Select all that apply)")
    .setChoiceValues([
      "Filtering organizations by tech stack / industry sector",
      "Viewing specific proposed training roles and expected skills before applying",
      "Submitting placement requests directly through the system",
      "Tracking the approval status of your placement request in real time",
      "Submitting a new organization for departmental vetting if not already listed"
    ])
    .showOtherOption(true)
    .setRequired(true);

  // Suggestions
  form.addParagraphTextItem()
    .setTitle("9. Any suggestions or comments to improve SIWES placement quality at BUK?")
    .setHelpText("Optional")
    .setRequired(false);

  // =======================================================================================
  // PUBLISH & LOG URLs
  // =======================================================================================
  const editUrl = form.getEditUrl();
  const publishedUrl = form.getPublishedUrl();

  Logger.log("================================================================================");
  Logger.log(" BUK-SIWES QOVRS STUDENT QUESTIONNAIRE CREATED SUCCESSFULLY!");
  Logger.log("================================================================================");
  Logger.log(" Form Title: " + formTitle);
  Logger.log(" Edit Form URL (for you to view/edit): \n" + editUrl);
  Logger.log("--------------------------------------------------------------------------------");
  Logger.log(" Published Form URL (send this to students): \n" + publishedUrl);
  Logger.log("================================================================================");

  return {
    formId: form.getId(),
    editUrl: editUrl,
    publishedUrl: publishedUrl
  };
}
