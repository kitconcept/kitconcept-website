import { ConfigType } from '@plone/registry';

export default function install(config: ConfigType) {
  // Volto Light Theme Configuration
  config.settings.siteHeader = true;
  config.settings.siteLabel = 'Site';

  return config;
}
