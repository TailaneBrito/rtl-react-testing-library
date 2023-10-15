//@ts-nocheck
import { sumPositiveNumbers } from "./example";

describe("When the arguments passed are positive numbers", () => {
    test("should return the right answer", () => {
        expect(sumPositiveNumbers(4,5)).toBe(9);
    });
    test('should throw an error', () => {
        let error;
        try{
            sumPositiveNumbers(-1, 5)
        } catch(err: any){
            error = err;
        }

        expect(error).toBeDefined();
        expect(error.message).toBe("One of the numbers are negative")
    })
})
export {}
