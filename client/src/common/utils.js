import moment from "moment";

export const errorHandler = errorResponse => {
  if (errorResponse && errorResponse.data && errorResponse.data.error) {
    return errorResponse.data.error.message;
  }
  return errorResponse;
};

export const utils = {
  processValidationError: errors => {
    const errorArray = errors.inner || [];
    const output = {};
    errorArray.forEach(err => {
      output[err.path] = err.message;
    });
    return output;
  },

  asyncForEach: async (array, callback) => {
    for (let index = 0; index < array.length; index = +1) {
      // eslint-disable-next-line no-await-in-loop
      await callback(array[index], index, array);
    }
  },
  formatDuration: duration => {
    let output = "";
    output += duration.years() ? `${duration.years()} Year(s) ` : "";
    output += duration.months() ? `${duration.months()} Month(s) ` : "";
    output += duration.days() ? `${duration.days()} Day(s) ` : "";
    output += duration.hours() ? `${duration.hours()} Hour(s) ` : "";
    output += duration.minutes() ? `${duration.minutes()} Minute(s) ` : "";
    output += duration.seconds() ? `${duration.seconds()} Second(s)` : "";
    return output;
  },

  debounce: (func, delay) => {
    let debounceTimer;
    return (...args) => {
      return new Promise((resolve, reject) => {
        const context = this;
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(
          () =>
            func
              .apply(context, args)
              .then(data => resolve(data))
              .catch(err => reject(err)),
          delay
        );
      });
    };
  },

  buttonize: handlerFn => {
    return {
      role: "button",
      onClick: handlerFn,
      onKeyDown: event => {
        // insert your preferred method for detecting the keypress
        if (event.keycode === 13) handlerFn(event);
      }
    };
  },
  processInlineEditValidationError: errors => {
    return errors.message;
  },

  isEmptyObject: obj => {
    return Object.keys(obj).length === 0;
  },

  defaultFilterMethod: (filter, row) => {
    let value = row[filter.id];
    if (value === undefined || value === null) {
      value = "";
    }
    value = String(value).toLowerCase();
    return value.includes(filter.value.toLowerCase());
  },

  createFinalString: (textArray, data) => {
    let output = "";
    textArray.forEach(text => {
      if (text.startsWith("<")) {
        const field = text.replace("<", "").replace(">", "");
        if (data.fields[field]) {
          output = `${output} ${data.fields[field]}`;
        }
      } else {
        output = `${output} ${text.trim()}`;
      }
    });
    return output.replace(/\s+/g, " ").trim();
  },

  buttonize: handlerFn => {
    return {
      role: "button",
      onClick: handlerFn,
      onKeyDown: event => {
        // insert your preferred method for detecting the keypress
        if (event.keycode === 13) handlerFn(event);
      }
    };
  },
  capitalizeFirstLetter: string => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  },
  uncapitalizeFirstLetter: string => {
    return string.charAt(0).toLowerCase() + string.slice(1);
  },
  truncateRecordName: (string, size) => {
    return string.length > (size || 10)
      ? `${string.substring(0, size || 10)}...`
      : string;
  },
  sortAutoId: (a, b) => {
    return (
      parseInt(a.substring(a.lastIndexOf("-") + 1), 10) -
      parseInt(b.substring(b.lastIndexOf("-") + 1), 10)
    );
  },

  dynamicColors: () => {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    return `rgb( ${r} , ${g} , ${b} )`;
  },
  calculateDifference: (endtime, startTime, time) => {
    const start = moment(startTime);
    const end = moment(endtime);
    const intervals = [
      "years",
      "months",
      "days",
      "hours",
      "minutes",
      "seconds"
    ];
    const outputObject = {};
    const outputString = [];

    intervals.forEach(ele => {
      const diff = end.diff(start, ele);
      start.add(diff, ele);
      if (diff && time.includes(ele)) {
        outputObject[ele] = diff;
        outputString.push(`${diff} ${ele}`);
      }
    });
    return { string: outputString.join(","), object: outputObject };
  }
};
