import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.withCredentials = true;

const coreApi = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BACKEND_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

coreApi.interceptors.request.use(
  (config) => {
    const access_token = Cookies.get("access_token");
    if (access_token) {
      config.headers.Authorization = `Bearer ${access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

coreApi.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const { response } = error;

    if (response && response.status === 401) {
      Cookies.remove("access_token");
      window.location.href = '/admin/sign-in';
    }

    return Promise.reject(error);
  }
);

export default coreApi;
