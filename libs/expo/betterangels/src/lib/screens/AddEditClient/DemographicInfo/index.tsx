import { Spacings } from '@monorepo/expo/shared/static';
import { Accordion } from '@monorepo/expo/shared/ui-components';
import { RefObject } from 'react';
import { ScrollView, View } from 'react-native';
import AdaAccommodation from './AdaAccommodation';
import EyeColor from './EyeColor';
import Gender from './Gender';
import HairColor from './HairColor';
import Height from './Height';
import MaritalStatus from './MaritalStatus';
import PhysicalDescription from './PhysicalDescription';
import PlaceOfBirth from './PlaceOfBirth';
import Pronoun from './Pronoun';
import Race from './Race';

interface IDemographicInfoProps {
  expanded: undefined | string | null;
  setExpanded: (expanded: undefined | string | null) => void;
  scrollRef: RefObject<ScrollView | null>;
}

export default function DemographicInfo(props: IDemographicInfoProps) {
  const { scrollRef, expanded, setExpanded } = props;

  const isDemographicInfo = expanded === 'Demographic Info';
  return (
    <Accordion
      scrollRef={scrollRef}
      expanded={expanded}
      setExpanded={() => {
        setExpanded(isDemographicInfo ? null : 'Demographic Info');
      }}
      mb="xs"
      title="Demographic Info"
    >
      {isDemographicInfo && (
        <View
          style={{
            height: isDemographicInfo ? 'auto' : 0,
            overflow: 'hidden',
            gap: Spacings.xs,
          }}
        >
          <Gender />
          <Pronoun />
          <Race />
          <PlaceOfBirth />
          <Height />
          <EyeColor />
          <HairColor />
          <MaritalStatus />
          <PhysicalDescription />
          <AdaAccommodation />
        </View>
      )}
    </Accordion>
  );
}
