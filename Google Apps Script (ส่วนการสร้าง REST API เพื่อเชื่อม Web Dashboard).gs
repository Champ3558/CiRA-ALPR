/******************************************************
 * AI Barrier Dashboard API
 * Version : 2.0
 ******************************************************/

const SPREADSHEET_ID = "1be0be3u2jUd74xxMejhS7D5WRAkytTsZyAxkau-XGjg";
const DATABASE_SHEET = "Database";
const LOG_SHEET = "Log";

/******************************************************
 * MAIN
 ******************************************************/

function doGet(e) {
  try {
    const action = safeString(e.parameter.action);
    switch (action) {
      case "getMembers":
        return getMembers();
      case "getLogs":
        return getLogs();
      case "info":
        return apiInfo();
      default:
        return jsonResponse(false, "Unknown Action", null);
    }
  } catch (err) {
    return jsonResponse(false, err.toString(), null);
  }
}

function doPost(e) {
  Logger.log(JSON.stringify(e.parameter));

  try {
    const action = safeString(e.parameter.action);
    const body = e.parameter;

    switch (action) {
      case "addMember":
        return addMember(body);

      case "updateMember":
        return updateMember(body);

      case "deleteMember":
        return deleteMember(body);

      default:
        return jsonResponse(false, "Unknown Action", null);
    }
  }
  catch (err) {
    return jsonResponse(false, err.toString(), null);
  }
}

/******************************************************
 * OPEN SHEET
 ******************************************************/

function databaseSheet() {
  return SpreadsheetApp
    .openById(SPREADSHEET_ID)
    .getSheetByName(DATABASE_SHEET);
}

function logSheet() {
  return SpreadsheetApp
    .openById(SPREADSHEET_ID)
    .getSheetByName(LOG_SHEET);
}

/******************************************************
 * JSON
 ******************************************************/

function jsonResponse(success, message, data) {
  return ContentService
    .createTextOutput(
      JSON.stringify({
        success: success,
        message: message,
        data: data
      })
    )
    .setMimeType(ContentService.MimeType.JSON);
}

/******************************************************
 * HELPER
 ******************************************************/

function safeString(value) {
  if (value === undefined) return "";
  if (value === null) return "";
  return String(value).trim();
}

function isEmpty(value) {
  return safeString(value) === "";
}

/******************************************************
 * GET MEMBERS
 ******************************************************/

function getMembers() {
  const sheet = databaseSheet();
  const values = sheet.getDataRange().getValues();
  if (values.length <= 1) {
    return jsonResponse(true, "Success", []);
  }
  const members = [];
  for (let i = 1; i < values.length; i++) {
    members.push({
      plate: safeString(values[i][0]),
      province: safeString(values[i][1]),
      member: safeString(values[i][2])
    });
  }
  return jsonResponse(true,"Success",members);
}

/******************************************************
 * GET LOGS
 ******************************************************/

function getLogs() {
  const sheet = logSheet();
  const values = sheet.getDataRange().getValues();
  if (values.length <= 1) {
    return jsonResponse(true, "Success", []);
  }
  const logs = [];
  for (let i = 1; i < values.length; i++) {
    logs.push({
      time: safeString(values[i][0]),
      plate: safeString(values[i][1]),
      province: safeString(values[i][2]),
      member: safeString(values[i][3]),
      servo: safeString(values[i][4]),
      remark: safeString(values[i][5])
    });
  }
  return jsonResponse(true, "Success", logs);
}

/******************************************************
 * ADD MEMBER
 ******************************************************/

function addMember(data) {
  try {
    const plate = safeString(data.plate);
    const province = safeString(data.province);
    const member = safeString(data.member);
    if (
      isEmpty(plate) ||
      isEmpty(member)
    ) {
      return jsonResponse(false, "Missing Data", null);
    }
    const sheet = databaseSheet();
    const values = sheet.getDataRange().getValues();

    // ตรวจสอบทะเบียนซ้ำ
    for (let i = 1; i < values.length; i++) {
      if (
        safeString(values[i][0]) === plate &&
        safeString(values[i][1]) === province
      ) {
        return jsonResponse(false, "Duplicate Data", null);
      }
    }
    sheet.appendRow([
      plate,
      province,
      member
    ]);
    return jsonResponse(true, "Member Added", null);
  }
  catch (err) {
    return jsonResponse(false, err.toString(), null);
  }
}

/******************************************************
 * UPDATE MEMBER
 ******************************************************/

function updateMember(data) {
  try {
    const oldPlate = safeString(data.oldPlate);
    const oldProvince = safeString(data.oldProvince);
    const plate = safeString(data.plate);
    const province = safeString(data.province);
    const member = safeString(data.member);
    if (
      isEmpty(oldPlate) ||
      isEmpty(plate) ||
      isEmpty(member)
    ) {
      return jsonResponse(false, "Missing Data", null);
    }
    const sheet = databaseSheet();
    const values = sheet.getDataRange().getValues();
    // ตรวจสอบข้อมูลซ้ำ (ยกเว้นแถวเดิม)
    for (let i = 1; i < values.length; i++) {
      const currentPlate = safeString(values[i][0]);
      const currentProvince = safeString(values[i][1]);
      if (
        currentPlate === plate &&
        currentProvince === province &&
        !(
          currentPlate === oldPlate &&
          currentProvince === oldProvince
        )
      ) {
        return jsonResponse(false, "Duplicate Data", null);
      }
    }
    // ค้นหาแถวที่ต้องการแก้ไข
    for (let i = 1; i < values.length; i++) {
      if (
        safeString(values[i][0]) === oldPlate &&
        safeString(values[i][1]) === oldProvince
      ) {
        sheet
          .getRange(i + 1, 1, 1, 3)
          .setValues([[
            plate,
            province,
            member
          ]]);
        return jsonResponse(true, "Member Updated", null);
      }
    }
    return jsonResponse(false, "Member Not Found", null);
  }
  catch (err) {
    return jsonResponse(false, err.toString(), null);
  }
}

/******************************************************
 * DELETE MEMBER
 ******************************************************/
function deleteMember(data) {
  Logger.log("plate = " + data.plate);
  Logger.log("province = " + data.province);
  Logger.log(JSON.stringify(data));
  try {
    const plate = safeString(data.plate);
    const province = safeString(data.province);

    if (isEmpty(plate)) {
      return jsonResponse(false, "TEST DELETE", null);
    }

    const sheet = databaseSheet();
    const values = sheet.getDataRange().getValues();
    for (let i = 1; i < values.length; i++) {
      if (
    safeString(values[i][0]) === plate &&
    (
        province === "" ||
        safeString(values[i][1]) === province
    )
      ) {
        sheet.deleteRow(i + 1);
        return jsonResponse(true, "Member Deleted", null);
      }
    }
    return jsonResponse(false, "Member Not Found", null);
  }
  catch (err) {
    return jsonResponse(false, err.toString(), null);
  }
}

/******************************************************
 * API INFO
 ******************************************************/

function apiInfo() {
  return jsonResponse(true, "Success", {
    project: "AI Barrier Dashboard API",
    version: "2.0",
    endpoints: [
      "getMembers",
      "getLogs",
      "addMember",
      "updateMember",
      "deleteMember"
    ]
  });
}

function testAPI() {
  Logger.log(apiInfo());
}
