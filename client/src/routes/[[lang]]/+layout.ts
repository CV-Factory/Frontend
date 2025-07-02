import { browser } from '$app/environment';
import { locale, waitLocale } from 'svelte-i18n';
import type { LayoutLoad } from './$types';
import '$lib/i18n'; // Import to initialize
import { error } from '@sveltejs/kit';

export const load: LayoutLoad = async ({ params }) => {
  const { lang: langParam } = params;

  // If lang is 'en' in the URL, it's a 404. Root URL '/' is for English.
  if (langParam === 'en') {
    throw error(404, 'Not Found');
  }

  // Define supported languages for URL paths
  const supportedLangs = ['ko'];

  // If a language is in the URL but not supported, it's a 404
  if (langParam && !supportedLangs.includes(langParam)) {
    throw error(404, 'Not Found');
  }

  const lang = langParam || 'en';
  if (browser) {
    locale.set(lang);
  }
  await waitLocale(lang);

  return { lang };
}; 