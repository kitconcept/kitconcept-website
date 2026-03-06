import { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installBlocks from './config/blocks';

const applyConfig = (config: ConfigType) => {
  installSettings(config);
  installBlocks(config);
  return config;
};

export default applyConfig;
