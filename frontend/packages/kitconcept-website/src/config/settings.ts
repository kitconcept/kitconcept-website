import { ConfigType } from '@plone/registry';
import newsSVG from '@plone/volto/icons/news.svg';

export default function install(config: ConfigType) {
  config.settings.supportedLanguages = ['de', 'en'];

  // Clear DSGVO add-on settings so it gets them from the `@site` endpoint
  const dsgvoSettings = config.settings.DSGVOBanner as {
    showBanner?: boolean;
    modules?: Array<string>;
  };
  delete dsgvoSettings.showBanner;
  delete dsgvoSettings.modules;
  config.settings.controlPanelsIcons['dsgvo-settings'] = newsSVG;

  // Volto Light Theme Configuration
  config.settings.siteHeader = true;
  config.settings.siteLabel = 'Site';

  return config;
}
