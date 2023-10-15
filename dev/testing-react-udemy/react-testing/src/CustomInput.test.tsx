// @ts-nocheck
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from "@testing-library/user-event";
import {jest} from '@jest/globals'
import CustomInput from './CustomInput';

describe('When everything is Ok', () => {
    test('should call the onChange callback handler when using the fireEvent function', () => {
        const onChange = jest.fn();
        render(
            <CustomInput value="" onChange={onChange}>
                Input: 
            </CustomInput>
        );

        fireEvent.change(screen.getByRole("textbox"), {
            target: { value: 'Tailane'}
        })

        expect(onChange).toHaveBeenCalledTimes(1);
    })

    test('should call the onChange callback handler when using the userEvent API', async () => {
        const onChange = jest.fn();
        render(
            <CustomInput value="" onChange={onChange}>
                Input: 
            </CustomInput>
        );

        await userEvent.type(screen.getByRole("textbox"), 'Tailane'); //for every key stroke, when pressed

        expect(onChange).toHaveBeenCalledTimes(7);
    });

    //test react component in integration
})