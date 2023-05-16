// Initializing
$(document).ready(function () {
  // SmartWizard initialize
  $("#smartwizard").smartWizard({
    // Other options...

    toolbarSettings: { toolbarPosition: "none" },
    // Add custom buttons for each step
  });
});
const localData = getFromLocalStorage("loginInfo", true);
// global declaration
// proId : step 1 create then for all other step update so we should have proId
let proId;

// first we will make sure Project Name and dates on first step we get

// update unit for multi dependancies
const updateUnits = function (e) {
  if (equipPrepDate.value && equipDelDate.value && clientId.value)
    selectVal(
      `/get/unitlist/?client=${clientId.value}&start_date=${equipPrepDate.value}&end_date=${equipDelDate.value}`,
      ["name_of_unit"],
      unitId,
      "Select Unit Name"
    );
};

// lets get everythin in step 1 :
const proName = getEle(".proName");
const equipPrepDate = getEle(".equipPrepDate");
const equipDelDate = getEle(".equipPDelDate");
const clientId = getEle("#clientName");
const unitId = getEle("#unitName");
const reactorId = getEle("#reactorName");
const proNum = getEle(".proNum");
const firstSubmit = getEle(".firstForm");
const backBtn = getAllEle(".goBack");

// step 2
const sow = getEle("#sow");
const contract = getEle("#contract");
const isSub = getEle(".scn");
const remark = getEle(".remark");
const secondSubmit = getEle(".secondStepForm");
// for whole thing related to isSub
const isSubGroup = getEle(".isSubG");
const errMsg = getEle(".errorMsg");

// step 3
const equipReady = getEle(".equipReady");
const equipshipC = getEle(".equipshipC");
const equipDeliveryC = getEle(".equipDeliveryC");
const proStart = getEle(".proStart");
const proEnd = getEle(".proEnd");
const equipReturn = getEle(".equipReturn");
const thirdSubmit = getEle(".thirdStepForm");
const createPBtn = getEle(".thirdStep");
// for modal thing
const myModal = getEle("#exampleModal");
const hModal = getEle(".modalBodyhead");
const pModal = getEle(".modalBodyP");
// now let's load all selectionvalue in projects
// 1 : for clien ids
selectVal(
  "/get/clientlist/",
  ["official_name"],
  clientId,
  "Select Client Name"
);

// for sow
selectVal(
  "/get/scopeofwork/",
  ["name"],
  sow,
  "Select Scope of work",
  "No Scope of work found"
);

// for static thing showing or hiding
contract.addEventListener("change", function (e) {
  if (e.target.value === "SUB") {
    isSubGroup.classList.remove("hidden");
  } else {
    isSubGroup.classList.add("hidden");
  }
});

// for equip prep date
equipPrepDate.addEventListener("change", function (e) {
  //   equipDelDate.value = "";
  equipDelDate.min = e.target.value;
  equipReady.min = e.target.value;
  equipshipC.min = e.target.value;
  equipDeliveryC.min = e.target.value;
  proStart.min = e.target.value;
  proEnd.min = e.target.value;
  equipReturn.min = e.target.value;
  if (
    equipDelDate.value &&
    new Date(equipDelDate.value).getTime() < new Date(e.target.value).getTime()
  ) {
    equipDelDate.value = "";
    // show some popup here
  }
});

equipDelDate.addEventListener("change", function (e) {
  //   equipDelDate.value = "";
  equipDelDate.max = e.target.value;
  equipReady.max = e.target.value;
  equipshipC.max = e.target.value;
  equipDeliveryC.max = e.target.value;
  proStart.max = e.target.value;
  proEnd.max = e.target.value;
  equipReturn.max = e.target.value;
});

// for units
clientId.addEventListener("change", updateUnits);
equipPrepDate.addEventListener("change", updateUnits);
equipDelDate.addEventListener("change", updateUnits);

// for reactors
unitId.addEventListener("change", function (e) {
  selectVal(
    `/get/reactor/?client=${clientId.value}&unit=${e.target.value}`,
    ["reactor_name"],
    reactorId,
    "Select Reactors",
    "No Reactors Found"
  );
});

backBtn.forEach((btn) => {
  btn.addEventListener("click", function () {
    $("#smartwizard").smartWizard("prev");
  });
});

const submitForm = async function (data, redirect = false) {
  let url, method;
  if (proId) {
    url = `/get/project/${proId}/`;
    method = "PATCH";
  } else {
    url = "/createproject/";
    method = "POST";
  }
  const response = await ajaxCall(
    url,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${localData.accessToken}`,
      },
      method: method,
      body: JSON.stringify(data),
      // signal,
    },
    8000
    // timeOutFunction
  );
  if (response.status === 200 || response.status === 201) {
    if (redirect) {
      window.location = "/project/all-project.html";
    }
    proId = response.data.id;
    return;
  }
  errMsg.textContent = `${response.status} Error Occured, Please try again`;
  // hModal.textContent = `${response.status} Error Occured`;
  // pModal.textContent = "Please Try Again";

  if (response.status === 401) {
    window.location = "login.html?login=0";
  }
};
firstSubmit.addEventListener("submit", async function (e) {
  e.preventDefault();
  $("#smartwizard").smartWizard("next");
  const firstStepData = {
    project_name: proName.value,
    project_number: proNum.value,
    equipment_prep: equipPrepDate.value,
    equipment_delivery_tubemaster: equipDelDate.value,
    client: clientId.value,
    unit: unitId.value,
    reactor: Array.from(reactorId.selectedOptions, (option) => option.value),
  };
  submitForm(firstStepData);
  // console.log(firstStepData);
  // now lets submit the data
  // console.log(response);
});

secondSubmit.addEventListener("submit", async function (e) {
  e.preventDefault();
  $("#smartwizard").smartWizard("next");
  const secondStepData = {
    scope_of_work: Array.from(sow.selectedOptions, (option) => option.value),
    contract: contract.value,
    if_sub_client_name: isSub.value,
    general_remarks: remark.value,
  };
  console.log(secondStepData);
  submitForm(secondStepData);
});

thirdSubmit.addEventListener("submit", async function (e) {
  e.preventDefault();
  // $("#smartwizard").smartWizard("next");
  const thirdStepData = {
    equipment_ready: equipReady.value,
    equipment_ship_client: equipshipC.value,
    equipment_delivery_client: equipDeliveryC.value,
    project_start: proStart.value,
    project_end: proEnd.value,
    equipment_return_tubemaster: equipReturn.value,
  };
  console.log(thirdStepData);
  // now lets change the text of the btns
  backBtn[backBtn.length - 1].disabled = true;
  createPBtn.disabled = true;
  createPBtn.textContent = "Adding Project";
  submitForm(thirdStepData, true);
});
