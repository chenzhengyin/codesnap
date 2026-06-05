import { ref, onMounted } from 'vue';

const PRO_KEY = 'codesnap_pro';

// Lemon Squeezy checkout URL - replace with your actual checkout link
export const LEMON_SQUEEZY_CHECKOUT_URL = 'https://codesnap.lemonsqueezy.com/checkout/buy/xxxxx';

export function usePro() {
  const isPro = ref(false);

  onMounted(() => {
    isPro.value = localStorage.getItem(PRO_KEY) === 'true';
    checkActivationFromURL();
  });

  function checkActivationFromURL() {
    const params = new URLSearchParams(window.location.search);
    if (params.get('activated') === 'success') {
      activatePro();
      window.history.replaceState({}, '', window.location.pathname);
    }
  }

  function activatePro() {
    localStorage.setItem(PRO_KEY, 'true');
    isPro.value = true;
    window.location.reload();
  }

  function openCheckout() {
    window.open(LEMON_SQUEEZY_CHECKOUT_URL, '_blank');
  }

  return {
    isPro,
    activatePro,
    openCheckout,
  };
}
