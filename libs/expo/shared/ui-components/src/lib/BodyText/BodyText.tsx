import { Colors } from '@monorepo/expo/shared/static';
import { ReactNode } from 'react';
import {
  GestureResponderEvent,
  StyleSheet,
  Text,
  TextStyle,
} from 'react-native';

const SIZES = {
  md: {
    fontSize: 16,
    lineHeight: 24,
  },
  sm: {
    fontSize: 14,
    lineHeight: 21,
  },
  xs: {
    fontSize: 11,
    lineHeight: 16.5,
  },
};

export function BodyText({
  children,
  textTransform,
  mb,
  mt,
  mr,
  ml,
  my,
  mx,
  onPress,
  textDecorationLine,
  color = Colors.DARK_BLUE,
  size = 'md',
  style,
}: {
  children: ReactNode;
  onPress?: ((event: GestureResponderEvent) => void) | undefined;
  textTransform?: 'none' | 'capitalize' | 'uppercase' | 'lowercase' | undefined;
  mb?: number;
  mt?: number;
  my?: number;
  mx?: number;
  ml?: number;
  mr?: number;
  textDecorationLine?:
    | 'none'
    | 'underline'
    | 'line-through'
    | 'underline line-through'
    | undefined;
  color?: string;
  size?: 'md' | 'sm' | 'xs';
  style?: TextStyle;
}) {
  return (
    <Text
      onPress={onPress}
      style={[
        styles.text,
        style,
        {
          textTransform,
          marginBottom: mb,
          marginTop: mt,
          marginLeft: ml,
          marginRight: mr,
          marginHorizontal: mx,
          marginVertical: my,
          textDecorationLine,
          color,
          fontSize: SIZES[size].fontSize,
          lineHeight: SIZES[size].lineHeight,
        },
      ]}
    >
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({
  text: {
    fontFamily: 'Pragmatica-book',
  },
});