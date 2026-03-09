import type { ConfigType } from '@plone/registry';
import type { StyleDefinition } from '@plone/types';
import { ContactListStylingSchema } from '../components/Blocks/ContactList/schema';

declare module '@plone/types' {
  export interface BlocksConfigData {
    contactList: BlockConfigBase;
  }

  export interface BlockConfigBase {
    themes?: StyleDefinition[];
    templates: {
      [key: string]: {
        label: string;
        template: any;
      };
    };
  }
}

export default function install(config: ConfigType) {
  config.blocks.blocksConfig.contactList.schemaEnhancer =
    ContactListStylingSchema;

  return config;
}
