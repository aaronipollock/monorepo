import { Colors, Spacings } from '@monorepo/expo/shared/static';
import { ReactElement, cloneElement, useState } from 'react';
import { ButtonProps, View } from 'react-native';
import BasicModal from '../BasicModal';
import Button from '../Button';
import TextBold from '../TextBold';
import TextButton from '../TextButton';
import TextRegular from '../TextRegular';

export default function RevertModal({
  title,
  body,
  onRevert,
  button,
}: {
  title: string;
  body: string;
  onRevert: () => void;
  button: ReactElement;
}) {
  const [visible, setVisible] = useState(false);

  const clonedButton = cloneElement(button as ReactElement<ButtonProps>, {
    onPress: () => {
      setVisible(true);
      if (button.props.onPress) {
        button.props.onPress();
      }
    },
  });

  return (
    <>
      {clonedButton}
      <BasicModal visible={visible} setVisible={setVisible}>
        <TextBold size="xl" mb="sm">
          {title}
        </TextBold>
        <TextRegular mb="md">{body}</TextRegular>
        <View
          style={{
            flexDirection: 'row',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <View
            style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}
          >
            <TextButton
              fontSize="sm"
              onPress={() => setVisible(false)}
              color={Colors.PRIMARY}
              accessibilityHint="continue to work on the note"
              title="Cancel"
            />
          </View>
          <View style={{ flex: 1, marginLeft: Spacings.xs }}>
            <Button
              size="full"
              accessibilityHint="reverts note to earlier state"
              onPress={async () => {
                onRevert();
                setVisible(false);
              }}
              variant="primary"
              title="Discard"
            />
          </View>
        </View>
      </BasicModal>
    </>
  );
}