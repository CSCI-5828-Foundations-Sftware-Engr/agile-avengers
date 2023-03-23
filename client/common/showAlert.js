import { toast } from "react-toastify";

export function showAlert(type, message) {
    switch (type) {
        case "success": {
            return toast.success(message, {
                position: toast.POSITION.TOP_CENTER,
                closeOnClick: true
            });
        }

        case "warning": {
            return toast.warning(message, {
                position: toast.POSITION.TOP_CENTER,
                closeOnClick: true
            });
        }

        case "error": {
            return toast.error(message, {
                position: toast.POSITION.TOP_CENTER,
                closeOnClick: true
            });
        }

        case "info": {
            return toast.info(message, {
                position: toast.POSITION.TOP_CENTER,
                closeOnClick: true
            });
        }

        case "default": {
            console.log("default show");
            return toast(message, {
                position: toast.POSITION.TOP_CENTER,
                closeOnClick: true
            });
        }
    }

}