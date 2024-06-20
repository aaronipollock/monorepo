import { Spacings } from '@monorepo/expo/shared/static';
import {
  BasicInput,
  BasicRadio,
  FieldCard,
  TextMedium,
} from '@monorepo/expo/shared/ui-components';
import { RefObject, useState } from 'react';
import { ScrollView, View } from 'react-native';
import { CreateClientProfileInput, GenderEnum } from '../../apollo';

interface IGenderProps {
  client: CreateClientProfileInput;
  setClient: (client: CreateClientProfileInput) => void;
  expanded: undefined | string | null;
  setExpanded: (expanded: undefined | string | null) => void;
  scrollRef: RefObject<ScrollView>;
}

const GENDERS: Array<'Male' | 'Female' | 'Other'> = ['Male', 'Female', 'Other'];

export default function Gender(props: IGenderProps) {
  const { expanded, setExpanded, client, setClient, scrollRef } = props;
  const [other, setOther] = useState(false);

  const isGender = expanded === 'Gender';

  return (
    <FieldCard
      scrollRef={scrollRef}
      expanded={expanded}
      setExpanded={() => {
        setExpanded(isGender ? null : 'Gender');
      }}
      mb="xs"
      actionName={
        !client.gender && !isGender ? (
          <TextMedium size="sm">Add Gender</TextMedium>
        ) : (
          <TextMedium textTransform="capitalize" size="sm">
            {client.gender}
          </TextMedium>
        )
      }
      title="Gender"
    >
      <View
        style={{
          gap: Spacings.sm,
          height: isGender ? 'auto' : 0,
          overflow: 'hidden',
        }}
      >
        <View
          style={{
            flexDirection: 'row',
            alignItems: 'center',
            gap: Spacings.sm,
          }}
        >
          {GENDERS.map((q) => (
            <BasicRadio
              label={q}
              accessibilityHint={`Select ${q}`}
              key={q}
              value={client.gender}
              onPress={() => {
                const isOther = q === 'Other';
                setOther(isOther);

                setClient({
                  ...client,
                  gender: q as GenderEnum,
                  otherGender: isOther ? client.otherGender : undefined,
                });
              }}
            />
          ))}
        </View>
        {other && (
          <BasicInput
            label="Other"
            value={client.otherGender}
            onChangeText={(e) =>
              setClient({
                ...client,
                otherGender: e,
              })
            }
          />
        )}
      </View>
    </FieldCard>
  );
}