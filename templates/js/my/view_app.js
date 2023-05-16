// usefull event handling functions
// to fetch data
const getAppData = async function (appId) {
  const localData = getFromLocalStorage("loginInfo", true);
  const response = await ajaxCall(
    `/applications/${appId}/`,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${localData.accessToken}`,
      },
      method: "GET",
    },
    8000
  );
  appName.innerHTML = response.data?.name?.student_name;
  assignedUser.innerHTML = response.data?.assigned_users?.username;
  appStatus.innerHTML = response.data?.status?.App_status;

  tenthMarksheet.src = response.data?.Tenth_Marksheet;
  twelvethMarksheet.src = response.data?.Twelveth_Marksheet;
  diploma.src = response.data?.Diploma_Marksheet;
  bachelor.src = response.data?.Bachelor_Marksheet;
  master.src = response.data?.Master_Marksheet;
  lor.src = response.data?.Lor;
  sop.src = response.data?.Sop;
  resume.src = response.data?.Resume;
  laexam.src = response.data?.Language_Exam;
  await selectVal(
    "/view-enquiry/",
    ["student_name"],
    appNameSelect,
    "Select Applicant",
    "No Applicant Found"
  );
  $(appNameSelect).val(response.data?.name?.id);

  await selectVal(
    "/userlist/",
    ["username"],
    assUserSelect,
    "Select User",
    "No users Found"
  );
  $(assUserSelect).val(response.data?.assigned_users?.id);
  await selectVal(
    "/appstatus/",
    ["App_status"],
    statusSelect,
    "Select App status",
    "No App status Found"
  );
  $(statusSelect).val(response.data?.status?.id);
  $(".selectpicker").selectpicker("refresh");
  return response.data;
};

const changeSelectionVal = async function (
  prop,
  appId,
  isFile,
  toggleEle,
  toggleEle2,
  e
) {
  const localData = getFromLocalStorage("loginInfo", true);

  const fdata = new FormData();
  let val;
  if (isFile) val = e.target.files[0];
  else val = +e.target.value;
  fdata.append(prop, val);

  const response = await ajaxCall(
    `/update-application/${appId}/`,
    {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${localData.accessToken}`,
      },

      body: fdata,
    },
    8000
  );
  console.log(response);
  await getAppData(appId);
  toggleHide(toggleEle, toggleEle2);
};

const addEvents = function (valDiv, selectDiv, selectEle, btn) {
  valDiv.addEventListener("dblclick", function () {
    toggleHide(valDiv, selectDiv);
    selectDiv.setAttribute("tabindex", "0");
    selectDiv.focus();
    console.log("focus");
  });
  btn.addEventListener("click", function () {
    toggleHide(valDiv, selectDiv);
  });
};

const toggleHide = (item1, item2) => {
  item1.classList.toggle("hide");
  item2.classList.toggle("hide");
};

// get id from url
const urlParams = new URLSearchParams(window.location.search);
const appId = urlParams.get("id");

// lets get all the fields

// export btn
const exportBtn = getEle(".exportBtn");
exportBtn.href = `https://flyurdream.online/pdf/${appId}`;
// main val div
const appName = getEle(".name");
const assignedUser = getEle(".assUsr");
const appStatus = getEle(".appStatus");

// select and edit div
const appNameEdit = getEle(".nameS");
const appNameSelect = getEle("#applicant");

const assUserEdit = getEle(".assUserS");
const assUserSelect = getEle("#assignedUser");

const appStatusEdit = getEle(".appStatusS");
const statusSelect = getEle("#status");

// cancel btns
const cancelNameBtn = getEle(".cancelNameBtn");
const cancelAuBtn = getEle(".cancelAuBtn");
const cancelSBtn = getEle(".cancelSBtn");

// selection of img
const tenthMarksheet = getEle(".tenth_marksheet");
const twelvethMarksheet = getEle(".twelvth_marksheet");
const diploma = getEle(".diploma");
const bachelor = getEle(".bachelor");
const master = getEle(".master");
const lor = getEle(".lor");
const sop = getEle(".sop");
const resume = getEle(".resume");
const laexam = getEle(".laexam");

// selection for document upload container
const tenthContainer = getEle(".tenth_marksheetContainer");
const twelvethContainer = getEle(".twelvth_marksheetContainer");
const diplomaContainer = getEle(".diplomaContainer");
const bachelorContainer = getEle(".bachelorContainer");
const masterContainer = getEle(".masterContainer");
const lorContainer = getEle(".lorContainer");
const sopContainer = getEle(".sopContainer");
const resumeContainer = getEle(".resumeContainer");
const laexamContainer = getEle(".laexamContainer");
// selection for document upload input
const tenthInput = getEle(".tenth_marksheetUpload");
const twelvethInput = getEle(".twelvth_marksheetUpload");
const diplomaInput = getEle(".diplomaUpload");
const bachelorInput = getEle(".bachelorUpload");
const masterInput = getEle(".masterUpload");
const lorInput = getEle(".lorUpload");
const sopInput = getEle(".sopUpload");
const resumeInput = getEle(".resumeUpload");
const laexamInput = getEle(".laexamUpload");

// for name
// addEvents(appName, appNameEdit, appNameSelect, cancelNameBtn);
// for assigned usr
addEvents(assignedUser, assUserEdit, assUserSelect, cancelAuBtn);
// for status
addEvents(appStatus, appStatusEdit, statusSelect, cancelSBtn);

// lets first get data
const appData = getAppData(appId);

// now for select option onchange

// appNameSelect.addEventListener(
//   "change",
//   changeSelectionVal.bind(null, "name", appId, false,)
// );
assUserSelect.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "assigned_users",
    appId,
    false,
    assignedUser,
    assUserEdit
  )
);
statusSelect.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "status",
    appId,
    false,
    appStatus,
    appStatusEdit
  )
);

// ok now handling the file thing
tenthMarksheet.addEventListener("dblclick", async function (e) {
  toggleHide(tenthMarksheet, tenthContainer);
});

twelvethMarksheet.addEventListener("dblclick", async function (e) {
  toggleHide(twelvethMarksheet, twelvethContainer);
});

diploma.addEventListener("dblclick", async function (e) {
  toggleHide(diploma, diplomaContainer);
});

bachelor.addEventListener("dblclick", async function (e) {
  toggleHide(bachelor, bachelorContainer);
});

master.addEventListener("dblclick", async function (e) {
  toggleHide(master, masterContainer);
});

lor.addEventListener("dblclick", async function (e) {
  toggleHide(lor, lorContainer);
});

sop.addEventListener("dblclick", async function (e) {
  toggleHide(sop, sopContainer);
});

resume.addEventListener("dblclick", async function (e) {
  toggleHide(resume, resumeContainer);
});

laexam.addEventListener("dblclick", async function (e) {
  toggleHide(laexam, laexamContainer);
});

// now for handling the file input

tenthInput.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "Tenth_Marksheet",
    appId,
    true,
    tenthMarksheet,
    tenthContainer
  )
);
twelvethInput.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "Twelveth_Marksheet",
    appId,
    true,
    twelvethMarksheet,
    twelvethContainer
  )
);
diplomaInput.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "Diploma_Marksheet",
    appId,
    true,
    diploma,
    diplomaContainer
  )
);
bachelorInput.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "Bachelor_Marksheet",
    appId,
    true,
    bachelor,
    bachelorContainer
  )
);
masterInput.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "Master_Marksheet",
    appId,
    true,
    master,
    masterContainer
  )
);
lorInput.addEventListener(
  "change",
  changeSelectionVal.bind(null, "Lor", appId, true, lor, lorContainer)
);
sopInput.addEventListener(
  "change",
  changeSelectionVal.bind(null, "Sop", appId, true, sop, sopContainer)
);
resumeInput.addEventListener(
  "change",
  changeSelectionVal.bind(null, "Resume", appId, true, resume, resumeContainer)
);
laexamInput.addEventListener(
  "change",
  changeSelectionVal.bind(
    null,
    "Language_Exam",
    appId,
    true,
    laexam,
    laexamContainer
  )
);
