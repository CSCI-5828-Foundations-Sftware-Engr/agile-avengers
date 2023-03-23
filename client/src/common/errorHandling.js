export const errorHandling = error => {
    if (error.response) {
        console.log(error.response);
        console.log("[errorHandling]:Response");
        console.log(error.response.data);
        return error.response.data;
    }
    console.log("[errorHandling]: No ERROR Response");
    console.log(JSON.stringify(error));
    return JSON.stringify(error);
};