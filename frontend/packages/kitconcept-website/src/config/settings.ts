import { ConfigType } from '@plone/registry';
import newsSVG from '@plone/volto/icons/news.svg';

export default function install(config: ConfigType) {
  config.settings.supportedLanguages = ['de', 'en'];

  config.settings.controlPanelsIcons['dsgvo-settings'] = newsSVG;

  // Volto Light Theme Configuration
  config.settings.siteHeader = true;
  config.settings.siteLabel = 'Site';

  return config;
}
