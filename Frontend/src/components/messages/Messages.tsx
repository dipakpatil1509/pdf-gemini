'use client';
/*eslint-disable*/

import MessageBoxChat from '@/components/MessageBox';
import { Button, Flex, Icon, Text, useColorModeValue } from '@chakra-ui/react';
import { MdOutlineFileCopy } from 'react-icons/md';
import { MdAutoAwesome, MdPerson } from 'react-icons/md';

const Messages = ({
    messages,
}: {
    messages: { content: string; role: string }[];
}) => {
    const borderColor = useColorModeValue('gray.200', 'whiteAlpha.200');
    const brandColor = useColorModeValue('brand.500', 'white');
    const textColor = useColorModeValue('navy.700', 'white');

    const copyToClipboard = (text: string) => {
        const el = document.createElement('textarea');
        el.value = text;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
    };

    return (
        <>
            <Flex
                direction="column"
                w="100%"
                mx="auto"
                display={messages.length > 0 ? 'flex' : 'none'}
                mb={'auto'}
            >
                {messages.map((message, id) =>
                    message.role === 'user' ? (
                        <Flex w="100%" align={'center'} mb="10px" key={id}>
                            <Flex
                                borderRadius="full"
                                justify="center"
                                align="center"
                                bg={'transparent'}
                                border="1px solid"
                                borderColor={borderColor}
                                me="20px"
                                h="40px"
                                minH="40px"
                                minW="40px"
                            >
                                <Icon
                                    as={MdPerson}
                                    width="20px"
                                    height="20px"
                                    color={brandColor}
                                />
                            </Flex>
                            <Flex
                                p="22px"
                                border="1px solid"
                                borderColor={borderColor}
                                borderRadius="14px"
                                w="100%"
                                zIndex={'2'}
                            >
                                <Text
                                    color={textColor}
                                    fontWeight="600"
                                    fontSize={{ base: 'sm', md: 'md' }}
                                    lineHeight={{ base: '24px', md: '26px' }}
                                >
                                    {message.content}
                                </Text>
                            </Flex>
                        </Flex>
                    ) : (
                        <Flex w="100%" key={id} mb="10px" position="relative">
                            <Flex
                                borderRadius="full"
                                justify="center"
                                align="center"
                                bg={'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%)'}
                                me="20px"
                                h="40px"
                                minH="40px"
                                minW="40px"
                            >
                                <Icon
                                    as={MdAutoAwesome}
                                    width="20px"
                                    height="20px"
                                    color="white"
                                />
                            </Flex>
                            <MessageBoxChat output={message.content} />
                            <Button
                                style={{ position: 'absolute', bottom: 0, right: 0 }}
                                onClick={() => {
                                    copyToClipboard(message.content);
                                }}
                                p={0}
                                _hover={""}
                                bg={"transparent"}
                            >
                                <Icon
                                    as={MdOutlineFileCopy}
                                    width="15px"
                                    height="15px"
                                    color={brandColor}
                                />
                            </Button>
                        </Flex>
                    ),
                )}
            </Flex>
        </>
    );
};

export default Messages;
