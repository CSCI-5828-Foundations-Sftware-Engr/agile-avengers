export const errorHandling = error => {
  if (error.response) {
    return error.response.data.message || error.response.data;
  }

  return JSON.stringify(error);
};
