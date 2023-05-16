async function authenticateUser(timeInMs, refreshToken) {
  const localData = getFromLocalStorage("loginInfo", true);
  if (localData === -1) {
    deleteFromLocalStorage("loginInfo");
    window.location = "/login.html";
  }
  console.log(localData);
  const hrPassed = Math.round(
    (Date.now() - localData.timeOfLogin) / 1000 / 60 / 60
  );
  const minPassed = Math.round(
    (Date.now() - localData.lastTokenDiff) / 1000 / 60
  );
  console.log("going inside", hrPassed, minPassed);
  if (minPassed >= 30 && hrPassed > 23) {
    console.log("time to logout");
    deleteFromLocalStorage("loginInfo");
    window.location = "/login.html";
  } else if (minPassed >= 30 && hrPassed < 24) {
    console.log("time to make req");
    const response = await ajaxCall(
      "/token/refresh/",
      {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        method: "POST",
        body: JSON.stringify({ refresh: localData.refreshToken }),
        // signal,
      },
      8000
    );
    console.log(response);
    const localData = getFromLocalStorage("loginInfo", true);
    if (!response?.data?.access.length) {
      deleteFromLocalStorage("loginInfo");
      window.location = "/login.html";
    } else {
      const localObj = {
        accessToken: response.data.access,
        refreshToken: localData.refreshToken,
        user_type: localData.user_type,
        userId: localData.userId,
        timeOfLogin: localData.timeOfLogin,
        lastTokenDiff: Date.now(),
        userName: localData.userName,
      };
      setToLocalStorage("loginInfo", localObj, true);
      setTimeout(() => authenticateUser(), 1000 * 60 * 30);
    }

    // return response;
  } else if (minPassed < 30) {
    console.log("no need to do anything");
    const newTime = 30 - minPassed;
    console.log("new Time in Min", newTime);
    setTimeout(() => authenticateUser(), 1000 * 60 * newTime);
  } else {
    console.log("hey");
  }
}
console.log("here");
authenticateUser();
