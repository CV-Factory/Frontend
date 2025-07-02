import { browser } from '$app/environment';
import { locale, waitLocale } from 'svelte-i18n';
import type { LayoutLoad } from './$types';
import '$lib/i18n'; // Import to initialize
import { redirect } from '@sveltejs/kit';

export const load: LayoutLoad = async ({ params }) => {
  if (params.lang === 'en') {
    throw redirect(301, '/');
  }

  const lang = params.lang || 'en';
  if (browser) {
    locale.set(lang);
  }
  await waitLocale(lang);

  return { lang };
}; 