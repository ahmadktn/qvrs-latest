/**
 * =========================================================================================
 * BUK-SIWES QOVRS: Requirements Elicitation Questionnaire Generator
 * Department of Software Engineering, Bayero University Kano (BUK)
 * Project: SIWES Quality, Organization Vetting and Rating System
 * =========================================================================================
 * 
 * DESCRIPTION:
 * This Google Apps Script creates a comprehensive, professional Requirements Elicitation
 * Questionnaire Google Form for the BUK-SIWES QOVRS project.
 * 
 * It models all four key stakeholders identified in Chapter 3 (Table 3.1 & Section 3.4.2):
 * 1. SIWES Coordinator / Departmental Administrators
 * 2. Academic Supervisors
 * 3. Students (Undergraduate Software Engineering SIWES candidates/returnees)
 * 4. Host Organization Representatives / Industry Supervisors
 * 
 * FEATURES:
 * - Dynamic branching: Respondents select their role and are guided to their specific section.
 * - Captures documented problems: Poor training quality, menial tasks, lack of organizational accountability.
 * - Evaluates proposed modules: Pre-placement vetting, approved directory, post-placement supervisor rating,
 *   running star aggregation, low-rating flagging, and blacklisting.
 * - Automatically configures form settings, publishes it, and logs both the Edit URL and Respondent URL.
 * 
 * HOW TO USE:
 * 1. Open Google Drive (drive.google.com) or Google Sheets.
 * 2. Visit script.google.com to open the Google Apps Script editor.
 * 3. Paste this entire script into the `Code.gs` file.
 * 4. Select `createBukSiwesQuestionnaire` from the function dropdown and click "Run".
 * 5. Grant the necessary permissions when prompted.
 * 6. View the Execution Log (View > Logs or Ctrl+Enter) to get your Form Edit & Response links.
 * =========================================================================================
 */

function createBukSiwesQuestionnaire() {
  const formTitle = "BUK-SIWES QOVRS: Requirements Elicitation Questionnaire";
  const formDescription = 
    "Bayero University Kano (BUK)\n" +
    "Faculty of Computing | Department of Software Engineering\n" +
    "Research Project: SIWES Quality, Organization Vetting and Rating System (BUK-SIWES QOVRS)\n\n" +
    "Dear Respondent,\n" +
    "This questionnaire is designed to elicit stakeholder requirements for the design and implementation of BUK-SIWES QOVRS. " +
    "The system addresses persistent challenges in SIWES implementation: poor training quality (students assigned menial, unrelated tasks " +
    "such as photocopying, running errands, or idle waiting) and zero organizational accountability (the lack of institutional mechanisms " +
    "to vet organizations beforehand or rate/blacklist low-performing organizations over successive sessions).\n\n" +
    "Your responses are strictly for academic research and system requirement analysis. Thank you for your valuable time.";

  // 1. Create Form
  const form = FormApp.create(formTitle);
  form.setDescription(formDescription);
  form.setConfirmationMessage("Thank you for your participation. Your feedback has been recorded and will directly inform the system requirements and design of the BUK-SIWES QOVRS platform.");
  form.setAllowResponseEdits(false);
  form.setAcceptingResponses(true);
  form.setShowLinkToRespondAgain(false);

  // =======================================================================================
  // SECTION 1: RESPONDENT DEMOGRAPHICS & ROLE SELECTION (Page 1)
  // =======================================================================================
  
  // Name (Optional)
  form.addTextItem()
    .setTitle("Full Name (Optional)")
    .setHelpText("You may provide your name or leave blank to respond anonymously.")
    .setRequired(false);

  // Email (Optional)
  form.addTextItem()
    .setTitle("Email Address (Optional)")
    .setHelpText("Provide if you would like to receive updates on the project.")
    .setRequired(false);

  // Department / Affiliation
  form.addTextItem()
    .setTitle("Department / Institutional Affiliation")
    .setHelpText("e.g., Software Engineering, Computer Science, Information Technology, or Company Name")
    .setRequired(true);

  // =======================================================================================
  // PRE-DECLARE SECTION BREAKS (Required for branching)
  // =======================================================================================
  const sectionStudent = form.addPageBreakItem().setTitle("Section 2: Student Requirements (SIWES Candidates & Returnees)");
  const sectionCoordinator = form.addPageBreakItem().setTitle("Section 3: SIWES Coordinator & Departmental Administrator Requirements");
  const sectionSupervisor = form.addPageBreakItem().setTitle("Section 4: Academic Supervisor Requirements");
  const sectionOrg = form.addPageBreakItem().setTitle("Section 5: Host Organization & Industry Representative Requirements");
  const sectionGeneral = form.addPageBreakItem().setTitle("Section 6: General Functional & Non-Functional System Requirements");

  // Add the Role Selector with Navigation Branching to Section 1
  const roleItem = form.addMultipleChoiceItem()
    .setTitle("Select Your Primary Stakeholder Role in the SIWES Process")
    .setHelpText("You will be directed to questions specifically tailored to your role.")
    .setRequired(true);

  roleItem.setChoices([
    roleItem.createChoice("Student (Undergraduate / SIWES Candidate or Returnee)", sectionStudent),
    roleItem.createChoice("SIWES Coordinator / Departmental Administrator", sectionCoordinator),
    roleItem.createChoice("Academic Supervisor", sectionSupervisor),
    roleItem.createChoice("Host Organization Representative / Industry Supervisor", sectionOrg)
  ]);

  // =======================================================================================
  // SECTION 2: STUDENT QUESTIONS
  // =======================================================================================
  sectionStudent.setHelpText(
    "This section captures student experiences regarding placement search, training quality, " +
    "curriculum relevance, and requirements for an approved directory."
  );

  form.addMultipleChoiceItem()
    .setTitle("[Student] What is your current academic level / SIWES status?")
    .setChoiceValues([
      "Pre-placement student (Preparing for SIWES)",
      "Currently undertaking SIWES placement",
      "Completed SIWES placement (Returned to 400L / 500L)"
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("[Student] How difficult was it for you to find an organization that offers genuine, curriculum-relevant Software Engineering / IT training?")
    .setChoiceValues([
      "Very Difficult - Most organizations had no relevant technical roles",
      "Moderately Difficult - Took substantial effort and trial-and-error",
      "Neutral / Average",
      "Easy - Found a suitable technical host organization quickly"
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle("[Student] In your experience or observation, which of the following issues occur during SIWES placements?")
    .setChoiceValues([
      "Students assigned menial tasks (photocopying, clerical errands, buying food)",
      "Long periods of idle waiting with no assigned work or projects",
      "Mismatch between host organization's business and Software Engineering curriculum",
      "Lack of qualified technical supervision or mentorship at the workplace",
      "Organization accepts students primarily as unpaid/cheap generic labor",
      "None of the above - Placements are consistently high quality"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addScaleItem()
    .setTitle("[Student] How valuable would a centralized 'Approved Organization Directory' be, where you can browse vetted organizations with past quality ratings before applying?")
    .setBounds(1, 5)
    .setLabels("Not Valuable At All", "Extremely Valuable")
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("[Student] Would you support a policy preventing students from applying to organizations that have been blacklisted or failed departmental vetting?")
    .setChoiceValues([
      "Strongly Support - Protects students from wasting their SIWES period on irrelevant tasks",
      "Support with conditions (e.g., student can appeal if they have a verified custom role)",
      "Neutral",
      "Oppose - Students should be allowed to place anywhere they find an acceptance letter"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("[Student] What specific features would you want in the student placement portal?")
    .setHelpText("e.g., Filtering by programming stack, viewing supervisor reviews, tracking placement request status.")
    .setRequired(false);

  // Set Student section to advance to Section 6
  sectionStudent.setGoToPage(sectionGeneral);

  // =======================================================================================
  // SECTION 3: SIWES COORDINATOR & DEPARTMENTAL ADMINISTRATOR QUESTIONS
  // =======================================================================================
  sectionCoordinator.setHelpText(
    "This section captures departmental administrative challenges in organization vetting, " +
    "tracking placement quality, and managing organization records over time."
  );

  form.addMultipleChoiceItem()
    .setTitle("[Coordinator] In the current process, does the department have a structured, institutional mechanism to vet organizations BEFORE students accept offers?")
    .setChoiceValues([
      "No - Process is largely reactive (approving acceptance letters after the student secures them)",
      "Partially - Informal review done manually on paper with no recorded criteria",
      "Yes - Fully structured institutional pre-placement vetting exists"
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("[Coordinator] Does the department currently maintain a cumulative, multi-year quality record or rating for host organizations?")
    .setChoiceValues([
      "No institutional memory exists - past experiences are lost once a cohort graduates",
      "Informal/tribal knowledge among individual staff members only",
      "Yes - A formal database tracks organization training track records"
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle("[Coordinator] Which criteria are most critical when vetting a host organization for Software Engineering students?")
    .setChoiceValues([
      "Relevance of organization's core business/services to Software Engineering",
      "Suitability and technical depth of the proposed training role",
      "Presence of qualified industry mentors/supervisors on-site",
      "Organizational training capacity and physical/technical facilities",
      "Historical supervisor ratings and track record from previous sessions",
      "Formal corporate registration (CAC / Legal status)"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("[Coordinator] What action should the system take when an organization's cumulative supervisor rating falls below the quality threshold (< 3.0 out of 5.0)?")
    .setChoiceValues([
      "Automatically flag for departmental review, with options to warn, monitor, or blacklist",
      "Automatically suspend the organization from the approved directory pending hearing",
      "Notify the coordinator via dashboard alert without changing organization status",
      "Other"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("[Coordinator] What administrative safeguards or workflows should be included before an organization is formally blacklisted?")
    .setHelpText("e.g., Requirement for documented supervisor evidence, coordinator review notes, appeal mechanism.")
    .setRequired(false);

  // Set Coordinator section to advance to Section 6
  sectionCoordinator.setGoToPage(sectionGeneral);

  // =======================================================================================
  // SECTION 4: ACADEMIC SUPERVISOR QUESTIONS
  // =======================================================================================
  sectionSupervisor.setHelpText(
    "This section captures academic supervisor perspectives on post-placement assessment, " +
    "curriculum alignment, and rating host organizations."
  );

  form.addMultipleChoiceItem()
    .setTitle("[Supervisor] Have you encountered cases during SIWES supervision where students were not engaged in curriculum-relevant software engineering tasks?")
    .setChoiceValues([
      "Frequently - Many organizations treat students as clerical or errand staff",
      "Occasionally - Some placements have weak technical exposure",
      "Rarely",
      "Never - All students observed were engaged in core software engineering"
    ])
    .setRequired(true);

  form.addCheckboxItem()
    .setTitle("[Supervisor] The proposed system evaluates organizations across 4 core post-placement dimensions. Do you agree these dimensions are sufficient?")
    .setChoiceValues([
      "Dimension 1: Skill Relevance (practical technical exposure vs menial tasks)",
      "Dimension 2: Supervision Adequacy (industry mentor commitment and guidance)",
      "Dimension 3: Curriculum Alignment (congruence with departmental curriculum)",
      "Dimension 4: Recommendation for Future Students (institutional endorsement)"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addScaleItem()
    .setTitle("[Supervisor] How important is it that your assessment of an organization directly updates a public/departmental 1-5 star quality rating?")
    .setBounds(1, 5)
    .setLabels("Not Important", "Crucial for Accountability")
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("[Supervisor] When should the post-placement assessment be triggered in the workflow?")
    .setChoiceValues([
      "Immediately once the student's placement is marked 'Completed' in the system",
      "During the supervisor's physical/virtual institutional visitation",
      "At the departmental defense / logbook grading period"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("[Supervisor] What additional qualitative feedback should supervisors record about host organizations?")
    .setHelpText("e.g., Work environment safety, tools/languages used, willingness to retain graduates.")
    .setRequired(false);

  // Set Supervisor section to advance to Section 6
  sectionSupervisor.setGoToPage(sectionGeneral);

  // =======================================================================================
  // SECTION 5: HOST ORGANIZATION & INDUSTRY REPRESENTATIVE QUESTIONS
  // =======================================================================================
  sectionOrg.setHelpText(
    "This section captures industry perspectives on registering with BUK, proposing training roles, " +
    "and receiving student placements."
  );

  form.addMultipleChoiceItem()
    .setTitle("[Organization] What is your organization's primary industry sector?")
    .setChoiceValues([
      "Software Engineering & Web/Mobile Development",
      "FinTech / Financial Services IT",
      "Telecommunications & Networking",
      "Cybersecurity & Infrastructure",
      "Public Sector IT / Government Agency",
      "Non-IT Industry with internal IT department"
    ])
    .showOtherOption(true)
    .setRequired(true);

  form.addScaleItem()
    .setTitle("[Organization] Would your organization find it convenient to submit company details and proposed training roles through an online departmental portal?")
    .setBounds(1, 5)
    .setLabels("Not Convenient", "Highly Convenient")
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("[Organization] Are you willing to provide a structured description of the specific engineering tasks and tools an intern will work on prior to student placement?")
    .setChoiceValues([
      "Yes - We already have defined internship job descriptions and mentors",
      "Yes - We can formulate this if provided clear departmental guidelines",
      "No - Work is assigned ad-hoc as needs arise"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("[Organization] What incentives or features would encourage reputable tech organizations to actively participate in the BUK-SIWES directory?")
    .setHelpText("e.g., Access to top-performing students, recognition on BUK departmental portal, fast-track hiring.")
    .setRequired(false);

  // Set Organization section to advance to Section 6
  sectionOrg.setGoToPage(sectionGeneral);

  // =======================================================================================
  // SECTION 6: GENERAL SYSTEM REQUIREMENTS & VALIDATION (Common to all)
  // =======================================================================================
  sectionGeneral.setHelpText(
    "This concluding section evaluates non-functional requirements and overall support " +
    "for the BUK-SIWES QOVRS closed-loop quality assurance concept."
  );

  form.addCheckboxItem()
    .setTitle("Which non-functional quality attributes do you consider most critical for this system?")
    .setChoiceValues([
      "Usability (Simple, responsive interface on both desktop and mobile devices)",
      "Security & Role-Based Access Control (Strict segregation between students, coordinators, supervisors)",
      "Transparency & Data Integrity (Tamper-proof ratings and clear audit history)",
      "Performance & Reliability (Fast response times during peak placement seasons)",
      "Fairness & Appeal Process (Preventing a single isolated review from unfair penalization)"
    ])
    .setRequired(true);

  form.addScaleItem()
    .setTitle("Overall, how strongly do you believe connecting Pre-Placement Vetting with Post-Placement Rating will improve SIWES quality at BUK?")
    .setBounds(1, 5)
    .setLabels("No Impact", "Transformative Impact")
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("Any additional recommendations, suggestions, or concerns regarding the BUK-SIWES QOVRS system?")
    .setRequired(false);

  // =======================================================================================
  // LOG LINKS FOR EDITING AND RESPONDING
  // =======================================================================================
  const editUrl = form.getEditUrl();
  const publishedUrl = form.getPublishedUrl();

  Logger.log("================================================================================");
  Logger.log(" BUK-SIWES QOVRS QUESTIONNAIRE GENERATED SUCCESSFULLY!");
  Logger.log("================================================================================");
  Logger.log(" Form Title: " + formTitle);
  Logger.log(" Edit Form URL (for Admin / Researcher): \n" + editUrl);
  Logger.log("--------------------------------------------------------------------------------");
  Logger.log(" Published Response URL (to share with respondents): \n" + publishedUrl);
  Logger.log("================================================================================");

  return {
    formId: form.getId(),
    editUrl: editUrl,
    publishedUrl: publishedUrl
  };
}
