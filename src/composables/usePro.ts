import { ref } from 'vue';

const PRO_KEY = 'codesnap_pro';

function getInitialProStatus(): boolean {
  const params = new URLSearchParams(window.location.search);
  if (params.get('activated') === 'success') {
    localStorage.setItem(PRO_KEY, 'true');
    window.history.replaceState({}, '', window.location.pathname);
    return true;
  }
  return localStorage.getItem(PRO_KEY) === 'true';
}

export function usePro() {
  const isPro = ref(getInitialProStatus());

  function activatePro() {
    localStorage.setItem(PRO_KEY, 'true');
    isPro.value = true;
  }

  return {
    isPro,
    activatePro,
  };
}
