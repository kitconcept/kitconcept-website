import { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  config.settings.isMultilingual = false;
  config.settings.supportedLanguages = ['en'];
  config.settings.defaultLanguage = 'en';

  // Volto Light Theme Configuration
  config.settings.siteHeader = true;
  config.settings.siteLabel = 'Site';

  return config;
}
