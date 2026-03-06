import { defaultStylingSchema } from '@kitconcept/volto-light-theme/components/Blocks/schema';
import type { JSONSchema, SchemaEnhancerArgs } from '@plone/types';
export const ContactListStylingSchema = ({
  schema,
  formData,
  intl,
}: SchemaEnhancerArgs): JSONSchema => {
  defaultStylingSchema({ schema, formData, intl });

  return schema;
};
