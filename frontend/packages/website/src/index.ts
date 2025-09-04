import { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installSlots from './config/slots';

declare module '@plone/types' {
  export interface GetSiteResponse {
    'kitconcept.website.custom_css': string;
  }
}

const applyConfig = (config: ConfigType) => {
  installSettings(config);
  installSlots(config);
  return config;
};

export default applyConfig;
