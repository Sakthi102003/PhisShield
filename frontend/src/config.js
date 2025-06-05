const removeTrailingSlash = (url) => url?.endsWith('/') ? url.slice(0, -1) : url;

export const config = {
  apiUrl: removeTrailingSlash(import.meta.env.VITE_API_URL) || 'http://localhost:5000'
};
