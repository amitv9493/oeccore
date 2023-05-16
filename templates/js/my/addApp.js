// so first select all infos

const applicant = getEle("#applicant");
const assignedUser = getEle("#assignedUser");
const statuss = getEle("#status");
const tenthMarksheet = getEle(".tenth");
const twelvethMarksheet = getEle(".twelth");
const diplomaMarksheet = getEle(".diploma");
const bachelorMarksheet = getEle(".bachlor");
const masterMarksheet = getEle(".master");
const lor = getEle(".lor");
const sop = getEle(".sop");
const resume = getEle(".resume");
const languageExam = getEle(".langExam");
const appBtn = getEle(".appBtn");
const appForm = getEle(".appForm");
// now we will load 3 selection items

selectVal(
  "/view-enquiry/",
  ["student_name"],
  applicant,
  "Select Applicant",
  "No Applicant Found"
);

selectVal(
  "/userlist/",
  ["username"],
  assignedUser,
  "Select User",
  "No users Found"
);
selectVal(
  "/appstatus/",
  ["App_status"],
  statuss,
  "Select App status",
  "No App status Found"
);

appForm.addEventListener("submit", async function (e) {
  appBtn.disabled = true;
  const localData = getFromLocalStorage("loginInfo", true);
  e.preventDefault();
  const fdata = new FormData();
  fdata.append("name", applicant.value);
  if (tenthMarksheet.files.length)
    fdata.append("Tenth_Marksheet", tenthMarksheet.files[0]);

  if (twelvethMarksheet.files.length)
    fdata.append("Twelveth_Marksheet", twelvethMarksheet.files[0]);

  if (diplomaMarksheet.files.length)
    fdata.append("Diploma_Marksheet", diplomaMarksheet.files[0]);

  if (bachelorMarksheet.files.length)
    fdata.append("Bachelor_Marksheet", bachelorMarksheet.files[0]);

  if (masterMarksheet.files.length)
    fdata.append("Master_Marksheet", masterMarksheet.files[0]);

  if (lor.files.length) fdata.append("Lor", lor.files[0]);

  if (sop.files.length) fdata.append("Sop", sop.files[0]);

  if (resume.files.length) fdata.append("Resume", resume.files[0]);

  if (languageExam.files.length)
    fdata.append("Language_Exam", languageExam.files[0]);

  fdata.append("assigned_users", assignedUser.value);
  fdata.append("status", statuss.value);
  const response = await ajaxCall(
    "/add-application/",
    {
      headers: {
        Authorization: `Bearer ${localData.accessToken}`,
      },
      method: "POST",
      body: fdata,
      // signal,
    },
    8000
  );
  if (response.status === 201) {
    window.location = "/application.html";
  }
  // timeOutFunction
});
