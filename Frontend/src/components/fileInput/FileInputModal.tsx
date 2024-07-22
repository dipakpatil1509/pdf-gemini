'use client';
import { useParams } from 'next/navigation';
import {
    Accordion,
    AccordionItem,
    AccordionButton,
    AccordionPanel,
    AccordionIcon,
    Box,
    Button,
    Flex,
    Icon,
    Input,
    Link,
    ListItem,
    UnorderedList,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalHeader,
    ModalOverlay,
    Text,
    useColorModeValue,
    useDisclosure,
    useToast,
    Textarea,
    Card,
} from '@chakra-ui/react';
import axios from 'axios';
import { useState } from 'react';
import { useRouter } from 'next/navigation';

function FileInputModal() {
    const params = useParams();

    const router = useRouter();

    const [fileToUpload, setFileToUpload] = useState<any>(null);
    const [inputCode, setInputCode] = useState<string>('');
	const [loading, setLoading] = useState<boolean>(false);

    const textColor = useColorModeValue('navy.700', 'white');
    const grayColor = useColorModeValue('gray.500', 'gray.500');
    const inputBorder = useColorModeValue('gray.200', 'whiteAlpha.200');
    const inputColor = useColorModeValue('navy.700', 'white');
    const toast = useToast();

    const handleSubmit = async () => {
        const formData = new FormData();
        formData.append('file', fileToUpload);
        formData.append('pdf_description', inputCode);
		setLoading(true);
        try {
            const response = await axios.post(
                process.env.NEXT_PUBLIC_API_URL + '/upload_file',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                },
            );
            console.log('File uploaded successfully:', response.data);
            
            toast({
                title: 'File Uploaded Successfully!',
                status: 'success',
                duration: 9000,
                isClosable: true,
            })
            router.push("/chat/" + response.data.data.pdf_chat_id)
        } catch (error) {
            console.error('Error uploading file:', error);
            toast({
                title: 'Something went wrong',
                description: error + "",
                status: 'error',
                duration: 9000,
                isClosable: true,
            })
        }
        setLoading(false);
    };

    return (
        <>
            <Modal blockScrollOnMount={false} isOpen={!params.id} onClose={() => { }}>
                <ModalOverlay />
                <ModalContent bg="none" boxShadow="none">
                    <Card textAlign={'center'}>
                        <ModalHeader
                            fontSize="22px"
                            fontWeight={'700'}
                            mx="auto"
                            textAlign={'center'}
                            color={textColor}
                        >
                            Upload your PDF file
                        </ModalHeader>
                        <ModalCloseButton _focus={{ boxShadow: 'none' }} />
                        <ModalBody p="0px">
                            <Text
                                color={grayColor}
                                fontWeight="500"
                                fontSize="md"
                                lineHeight="28px"
                                mb="22px"
                            >
                                Please add some description for better results
                            </Text>
                            <Flex mb="20px" wrap="wrap" px="10px">
                                <Input
                                    h="100%"
                                    w="100%"
                                    border="1px solid"
                                    borderColor={inputBorder}
                                    borderRadius="15px"
                                    p="15px 20px"
                                    fontSize="sm"
                                    fontWeight="500"
                                    my="5px"
                                    _focus={{ borderColor: 'none' }}
                                    _placeholder={{ color: 'gray.500' }}
                                    color={inputColor}
                                    type="file"
                                    onChange={(e: any) => setFileToUpload(e.target.files[0])}
                                />
                                <Textarea
                                    h="100%"
                                    w="100%"
                                    border="1px solid"
                                    borderColor={inputBorder}
                                    borderRadius="15px"
                                    p="15px 20px"
                                    my="5px"
                                    fontSize="sm"
                                    fontWeight="500"
                                    _focus={{ borderColor: 'none' }}
                                    _placeholder={{ color: 'gray.500' }}
                                    color={inputColor}
                                    placeholder="PDF Description"
                                    onChange={(e: any) => setInputCode(e.target.value)}
                                    value={inputCode}
                                />
                                <Button
                                    variant="chakraLinear"
                                    py="20px"
                                    px="16px"
                                    fontSize="sm"
                                    borderRadius="15px"
                                    mx="auto"
                                    mt="20px"
                                    mb={{ base: '20px', md: '0px' }}
                                    w={{ base: '300px', md: '180px' }}
                                    h="54px"
                                    onClick={handleSubmit}
                                    isLoading={loading}
                                >
                                    Upload File
                                </Button>
                            </Flex>
                        </ModalBody>
                    </Card>
                </ModalContent>
            </Modal>
        </>
    );
}

export default FileInputModal;
