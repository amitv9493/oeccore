async function selectVal(
  url,
  keys,
  selectedClss,
  val,
  emptyVal = "No Data for Selected value"
) {
  const localData = getFromLocalStorage("loginInfo", true);
  const response = await ajaxCall(
    url,
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
  console.log(response);
  let options = "";
  //   for(){}
  if (!response.data?.length) {
    selectedClss.setAttribute("title", emptyVal);
    $(".selectpicker").selectpicker("refresh");
    return;
  }
  selectedClss.required = true;
  response.data.forEach((ele) => {
    let optionName = "";
    keys.forEach((data) => (optionName += ele[data] + " "));
    options += `<option value=${ele.id}>${optionName}</option>`;
  });
  console.log(options);
  selectedClss.innerHTML = options;
  selectedClss.title = val;
  $(".selectpicker").selectpicker("refresh");
}
