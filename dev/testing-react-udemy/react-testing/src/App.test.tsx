// @ts-nocheck
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from "@testing-library/user-event";
import App from './App';
import { getUser } from './get-user';
import {jest} from '@jest/globals'


jest.mock('./get-user'); 
const mockGetUser = jest.mocked(getUser, true);

describe("When everything renders", () => {

    beforeEach(async() => { //before each test render app
        // eslint-disable-next-line testing-library/no-render-in-setup
        render(<App />);
        await waitFor(() => expect(mockGetUser).toHaveBeenCalled()) //awaits for the api getUser to be called.
    })

    test("should render the app component without crashing", () => {  
        // eslint-disable-next-line testing-library/no-debugging-utils
        screen.debug();
    });

    test('should select the children that is being passed to the CustomInput component', () => {
        // screen.getByText('Input:');
        // screen.getByText(/Input:/); //passing a regular expression

        screen.getAllByText('Input:');

        screen.getAllByText(/Input:/); //passing a regular expression
        
        // testing if a text is not in the document
        let error
        try{
            expect(screen.getByText('Input')).toBeInTheDocument();
        }catch(err){
            error = err
        }
        expect(error).toBeDefined();
        
    });

    test('should select the input element by its role', () => {
        // screen.getByRole('textbox') //implicity assertion
        // expect(screen.getByRole('textbox')).toBeInTheDocument();

        screen.getAllByRole('textbox') //implicity assertion
        expect(screen.getAllByRole('textbox')[0]).toBeInTheDocument();
        expect(screen.getAllByRole('textbox').length).toEqual(1); //implicit assertion
    })

    test('should select a label element by its text', () => {
        // screen.getByLabelText('Input:') //search by label component
        // screen.getAllByText(/Input/); //gets all elements with input
        screen.getAllByText(/Input/); //gets all elements with input
    })

    test('should select input elemeny by placeholder text', () => {
        // screen.getByPlaceholderText('Example');
        screen.getAllByPlaceholderText('Example');
    })

    test('should not find the role "whatever" in our component', () => {
        expect(screen.queryByRole('whatever')).toBeNull()
    })
    
})

describe("whe the component fetches the user successfully", () => {
    beforeEach(() => {
        mockGetUser.mockClear()
    });

    test("should call getUser once", async () => {
        render(<App />);
        await waitFor(() => expect(mockGetUser).toHaveBeenCalledTimes(1)) //ensures the api has been called once
    });

    test("should render the username passed", async() => {
        const name = 'John'
        mockGetUser.mockResolvedValueOnce({ id: '1', name})
        // mockGetUser.mockImplementationOnce(() => Promise.resolve({id: 1, name})) //same thing as above
        render(<App />);
        expect(screen.queryByText(/Username/)).toBeNull();
        // expect(await screen.findByText(/name/)).toBeInTheDocument(); slight bug: it will find "Username" instead of 'John'
        // screen.debug(); // help finding errors
        expect(await screen.findByText(`Username: ${name}`)).toBeInTheDocument();
    })
})

describe("When the user enters some text in the input element", () => {
    it('should display the text in the screen', async () => {
        //user effect being used, so we need to wait for something.
        render(<App />)
        await waitFor(() => expect(mockGetUser).toHaveBeenCalled());

        // eslint-disable-next-line jest/valid-expect
        expect(screen.getByText(/You typed: .../));


        // fireEvent.change(screen.getByRole("textbox"), {
        //     target: { value: 'Tailane'}
        // })

        await userEvent.type(screen.getByRole('textbox'), 'Tailane')

        // eslint-disable-next-line jest/valid-expect
        expect(screen.getByText(/You typed: Tailane/));
    });

    
})