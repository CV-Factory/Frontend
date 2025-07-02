import { browser } from '$app/environment';
import { init, register } from 'svelte-i18n';

const defaultLocale = 'en';

register('en', () => import('./en.json'));
register('ko', () => import('./ko.json'));

init({
  fallbackLocale: defaultLocale,
  initialLocale: defaultLocale,
}); 