// import { ajaxCall } from "./modules/fetch";

// get all things first
const userName = getEle(".userName");
const pass = getEle(".pass");
const loginForm = getEle(".loginForm");

loginForm.addEventListener("submit", async function (e) {
  e.preventDefault();
  console.log("hello");
  const jsonPost = JSON.stringify({
    username: userName.value,
    password: pass.value,
  });
  const controller = new AbortController();
  const signal = controller.signal;
  const loginResponse = await ajaxCall(
    "/user/login/",
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: jsonPost,
      signal,
    },
    8000
  );
  console.log(loginResponse);
  const loginData = {
    accessToken: loginResponse.data?.token?.access,
    refreshToken: loginResponse.data?.token?.refresh,
    user_type: loginResponse.data?.user_status,
    userId: loginResponse.data?.userid,
    timeOfLogin: Date.now(),
    lastTokenDiff: Date.now(),
    userName: userName.value,
  };
  setToLocalStorage("loginInfo", loginData, true);
  window.location = "/index.html";
});
