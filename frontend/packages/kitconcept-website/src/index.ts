import { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installBlocks from './config/blocks';
import PersonView from './components/theme/PersonView';

const applyConfig = (config: ConfigType) => {
  installSettings(config);
  installBlocks(config);

  config.views.contentTypesViews.Person = PersonView;

  return config;
};

export default applyConfig;
