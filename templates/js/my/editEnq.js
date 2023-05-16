const getData = async (enqId) => {
  const localData = getFromLocalStorage("loginInfo", true);
  const response = await ajaxCall(
    `/enquiries/${enqId}/`,
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: `Bearer ${localData.accessToken}`,
      },
      method: "PATCH",
    },
    8000
  );
  console.log(response);
  setData(student_name, response.data.student_name);
  setData(student_phone, response.data.student_phone);
  setData(student_email, response.data.student_email);
  setData(student_address, response.data.student_address);
  setData(passport_number, response.data.passport_number);
  setData(married, response.data.married);
  setData(nationality, response.data.nationality);
  setData(dob, response.data.dob);
  setData(currentEdu, response.data.current_education.id);
  setData(countryInt, response.data.country_interested.id);
  setData(uniInterested, response.data.university_interested.id);
  setData(levelAppF, response.data.level_applying_for.id);
  setData(courseInt, response.data.course_interested.id);
  setData(IntakeInt, response.data.intake_interested.id);
  setData(notes, response.data.notes);
  setData(assignedU, response.data.assigned_users.id);
  setData(enqStatus, response.data.enquiry_status.id);
};

const setData = (ele, val) => (ele.value = val);
$(document).ready(function () {
  // SmartWizard initialize
  $("#smartwizard").smartWizard({
    // Other options...

    toolbarSettings: { toolbarPosition: "none" },
    // Add custom buttons for each step
  });
});
$(".dropdown").on("show.bs.dropdown", function () {
  $("body").append(
    $(".dropdown")
      .css({
        position: "absolute",
        left: $(".dropdown").offset().left,
        top: $(".dropdown").offset().top,
      })
      .detach()
  );
});
// global enqId to see whether update or create

// lets first get all steps data

// backbtn :
const backBtn = getAllEle(".goBack");
// first step
const student_name = getEle(".sName");
const student_phone = getEle(".sPhone");
const student_email = getEle(".sEmail");
const student_address = getEle(".sAddress");
const passport_number = getEle(".PassN");
const married = getEle("#isMarried");
const nationality = getEle(".nationality");
const dob = getEle(".dob");

// selectionbox
const currentEdu = getEle("#currentEdu");
const countryInt = getEle("#countryInt");
const studentInfoForm = getEle(".studentInfoForm");
// second step
const uniInterested = getEle("#uniInterested");
const levelAppF = getEle("#levelAppF");
const courseInt = getEle("#courseInt");
const IntakeInt = getEle("#IntakeInt");
const notes = getEle(".notes");
const course_infoForm = getEle(".course_info");
// third step
const assignedU = getEle("#assignedU");
const enqStatus = getEle("#enqStatus");
const assigned_enqForm = getEle(".assigned_enq");

// errr msg
const errMsg = getEle(".errorMsg");

// first get data
const urlParams = new URLSearchParams(window.location.search);
const enqID = urlParams.get("id");
getData(enqID);
// backbtn thing
backBtn.forEach((btn) => {
  btn.addEventListener("click", function () {
    $("#smartwizard").smartWizard("prev");
  });
});

// now let's get currentedu and country data as we need it when we load page
document.addEventListener("DOMContentLoaded", function (event) {
  // your code here
  selectVal(
    "/currenteducation/",
    ["current_education"],
    currentEdu,
    "Select Educations",
    "No Educations Found"
  );
  selectVal(
    "/countries/",
    ["country_name"],
    countryInt,
    "Select Country",
    "No Country Found"
  );
  selectVal(
    "/universitieslists/",
    ["univ_name"],
    uniInterested,
    "Select University",
    "No University Found"
  );
  selectVal(
    "/courselevels/",
    ["levels"],
    levelAppF,
    "Select Levels",
    "No Levels Found"
  );
  selectVal(
    "/intakes/",
    ["intake_month", "intake_year"],
    IntakeInt,
    "Select Intakes",
    "No Intakes Found"
  );
  selectVal(
    "/userlist/",
    ["username"],
    assignedU,
    "Select Intakes",
    "No Intakes Found"
  );
  selectVal(
    "/enquirystatus/",
    ["status"],
    enqStatus,
    "Select Intakes",
    "No Intakes Found"
  );
});

const updateCourses = function (e) {
  if (uniInterested.value && levelAppF.value)
    selectVal(
      `/courseslists/?university=${uniInterested.value}&course_levels=${levelAppF.value}`,
      ["course_name"],
      courseInt,
      "Select Course Name"
    );
};

// for units
uniInterested.addEventListener("change", updateCourses);
levelAppF.addEventListener("change", updateCourses);

// submit first form
studentInfoForm.addEventListener("submit", function (e) {
  e.preventDefault();
  $("#smartwizard").smartWizard("next");
  formData = {
    student_name: student_name.value,
    student_phone: student_phone.value,
    student_email: student_email.value,
    student_address: student_address.value,
    passport_number: passport_number.value,
    married: married.value,
    nationality: nationality.value,
    dob: dob.value,
    current_education: currentEdu.value,
    country_interested: countryInt.value,
  };
  submitForm(formData);
});

// submit second form
course_infoForm.addEventListener("submit", function (e) {
  e.preventDefault();
  $("#smartwizard").smartWizard("next");
  formData = {
    university_interested: uniInterested.value,
    level_applying_for: levelAppF.value,
    course_interested: courseInt.value,
    intake_interested: IntakeInt.value,
    notes: notes.value,
  };
  submitForm(formData);
});

// submit third form
assigned_enqForm.addEventListener("submit", function (e) {
  e.preventDefault();
  formData = {
    assigned_users: assignedU.value,
    enquiry_status: enqStatus.value,
  };
  backBtn[backBtn.length - 1].disabled = true;
  createPBtn.disabled = true;
  createPBtn.textContent = "Adding Project";
  submitForm(formData, true);
});

// main submit Btn
const submitForm = async function (data, redirect = false) {
  const localData = getFromLocalStorage("loginInfo", true);
  const url = `/update-enquiry/${enqID}/`;
  const method = "PATCH";
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
      window.location = "/enquiry.html";
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
