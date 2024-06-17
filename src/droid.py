from modules.smokers.SGopenSmoker import SGopenSmoker
from modules.smokers.PanAuthSmoker import PanAuthSmoker
from modules.smokers.AWSadminSmoker import AWSadminSmoker
from modules.smokers.awsConsoleAuthSmoker import awsConsoleAuthSmoker
from modules.smokers.CTrailSmoker import CTrailSmoker
from modules.smokers.S3PublicSmoker import S3PublicSmoker
from modules.smokers.EBSPublicSmoker import EBSPublicSmoker
from modules.smokers.test_logger import test_message
from modules.welcome import home
from modules.logs import siras_logger, siras_s3_logger

import argparse


def main(args):
    if args['bucket'] == 'True':
        siras_s3_logger('siras')
    elif args['bucket'] == 'False':
        siras_logger('siras')
    else:
        print('Please provide the correct arguments to run the siras')

    if args['smoker'] == 'test':
        test_message()
    elif args['smoker'] == 'sg':
        SGopenSmoker()
    elif args['smoker'] == 'pa':
        PanAuthSmoker()
    elif args['smoker'] == 'au':
        AWSadminSmoker()
    elif args['smoker'] == 'aca':
        awsConsoleAuthSmoker()
    elif args['smoker'] == 'ctr':
        CTrailSmoker()
    elif args['smoker'] == 's3p':
        S3PublicSmoker()
    elif args['smoker'] == 'esb':
        EBSPublicSmoker()
    elif args['smoker'] == 'all':
        smokers = [
            SGopenSmoker,
            PanAuthSmoker,
            AWSadminSmoker,
            awsConsoleAuthSmoker,
            CTrailSmoker,
            S3PublicSmoker,
            EBSPublicSmoker
        ]
        for smoker in smokers:
            smoker()


if __name__ == '__main__':
    home()
    print('Cloud Incident and Response Simulations. Lets you perform tabletop exercises, which measures the effectiveness in defining the incident response plan. It works as a red/purple-team-as-code, which checks if your security posture is adequate.\n\n https://github.com/cloud-sniper/siras.\n\n')
    siras_parser = argparse.ArgumentParser()
    siras_parser.version = 'version: 2.0 - https://github.com/cloud-sniper/siras'
    siras_parser.add_argument(
        '-s', help='smoker to run', dest='smoker', type=str, required=True)
    siras_parser.add_argument(
        '-b', help='save the results into a bucket', dest='bucket', type=str, required=True)
    args = siras_parser.parse_args()
    event_map = {'smoker': args.smoker, 'bucket': args.bucket}
    main(event_map)
