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
    const accessToken = Cookies.get("accessToken");
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
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
  async (error) => {
    const { response } = error;

    if (response && response.status === 401) {
      Cookies.remove("accessToken");
      Cookies.remove("refreshToken");

      window.location.href = '/sign-in';

      return Promise.reject(error);
    }
  }
);

export default coreApi;
