import hex_tool
import csv

config_name_map = {
    "标定参数零件号左后": "CalibrationPartNumberRearLeft",
    "配置形态": "ConfigurationMode",
    "功能有无": "FunctionAvailability",
    "默认开启": "DefaultEnabled",
    "上下电记忆": "PowerOnOffMemory",
    "拖车左右舵": "TrailerSteeringType",
    "标定参数版本号": "CalibrationVersion",
    "是否有DOW灯": "DOWLightPresent",
    "白天PWM_Duty": "DaytimePwmDuty",
    "黑夜PWM_Duty": "NighttimePwmDuty",
    "射频可关闭功能": "RFSwitchable",
    "DOW三级功能使能": "DOWLevel3Enabled",
    "RAEB功能使能": "RAEBEnabled",
    "VehicleType": "VehicleType",
    "IsManualgear": "IsManualgear",
    "ObjectInf2CANKey": "ObjectInf2CANKey",
    "version1": "version1",
    "version2": "version2",
    "雷达ID号": "RadarID",
    "ELK方案选择": "ELKSolutionSelect",
    "CIRAlarmVersionNo": "CIRAlarmVersionNo",
    "CIRAlarmSubVersionNo": "CIRAlarmSubVersionNo",
    "minDisXBSD": "minDisXBSD",
    "maxDisXBSD": "maxDisXBSD",
    "minDisYBSD": "minDisYBSD",
    "maxDisYBSD": "maxDisYBSD",
    "minDisXDOW": "minDisXDOW",
    "midDisXDOW": "midDisXDOW",
    "maxDisXDOW": "maxDisXDOW",
    "minDisYDOW": "minDisYDOW",
    "midDisYDOW": "midDisYDOW",
    "maxDisYDOW": "maxDisYDOW",
    "dangareaXDOW": "dangerAreaXDOW",
    "dangareaYDOW": "dangerAreaYDOW",
    "minDisXLCA": "minDisXLCA",
    "maxDisXLCA": "maxDisXLCA",
    "minDisYLCA": "minDisYLCA",
    "maxDisYLCA": "maxDisYLCA",
    "BSDEnableSpeed": "BSDEnableSpeed",
    "BSDStandbySpeed": "BSDStandbySpeed",
    "BSDEnableSpeed_MAX": "BSDEnableSpeed_MAX",
    "BSDResTrainSpeed": "BSDResTrainSpeed",
    "BSDDelayDisY": "BSDDelayDisY",
    "LCAEnableSpeed": "LCAEnableSpeed",
    "LCAStandbySpeed": "LCAStandbySpeed",
    "LCAEnableSpeed_MAX": "LCAEnableSpeed_MAX",
    "DOWEnableSpeed": "DOWEnableSpeed",
    "DOWLimitSpeed": "DOWLimitSpeed",
    "RCTAEnableSpeed": "RCTAEnableSpeed",
    "RCTALimitSpeed": "RCTALimitSpeed",
    "minDisXRCTA": "minDisXRCTA",
    "maxDisXRCTA": "maxDisXRCTA",
    "minDisYRCTA": "minDisYRCTA",
    "maxDisYRCTA": "maxDisYRCTA",
    "R1_RCTA": "R1_RCTA",
    "R2_RCTA": "R2_RCTA",
    "RctaInnerAngle": "RctaInnerAngle",
    "RctaOuterAngle": "RctaOuterAngle",
    "ttcLCA": "ttcLCA",
    "ttcLCA1": "ttcLCA1",
    "ttcLCA2": "ttcLCA2",
    "ttcRCTA": "ttcRCTA",
    "ttcDOW": "ttcDOW",
    "RCWEnableSpeed": "RCWEnableSpeed",
    "RCWEndSpeed": "RCWEndSpeed",
    "minDisXRCW": "minDisXRCW",
    "maxDisXRCW": "maxDisXRCW",
    "minDisYRCW": "minDisYRCW",
    "maxDisYRCW": "maxDisYRCW",
    "ttcRCW": "ttcRCW",
    "VelTres1RCW": "VelTres1RCW",
    "VelTres2RCW": "VelTres2RCW",
    "ttcRCTB": "ttcRCTB",
    "LatinNCAP_Delay_t": "LatinNCAP_Delay_t",
    "reserve0": "reserve0",
    "ELKAResTrainSpeedHigh": "ELKAResTrainSpeedHigh",
    "ELKAResTrainSpeedLow": "ELKAResTrainSpeedLow",
    "ELKBResTrainSpeedHigh": "ELKBResTrainSpeedHigh",
    "ELKBResTrainSpeedLow": "ELKBResTrainSpeedLow",
    "BSDDelayFrameno": "BSDDelayFrameno",
    "Vversion1": "Vversion1",
    "Vversion2": "Vversion2",
    "VehicleLength": "VehicleLength",
    "VehicleWidth": "VehicleWidth",
    "RealWheelsDistance": "RealWheelsDistance",
    "RearLeft_RadarPos_X": "RearLeft_RadarPos_X",
    "RearLeft_RadarPos_Y": "RearLeft_RadarPos_Y",
    "RearLeft_RadarPos_Z": "RearLeft_RadarPos_Z",
    "RearLeft_PitchNear": "RearLeft_PitchNear",
    "RearLeft_RollNear": "RearLeft_RollNear",
    "RearLeft_YawNear": "RearLeft_YawNear",
    "RearLeft_ConnectorDiretion": "RearLeft_ConnectorDirection",
    "RearLeft_INSTALL_ANGLE": "RearLeft_INSTALL_ANGLE",
    "RearRight_RadarPos_X": "RearRight_RadarPos_X",
    "RearRight_RadarPos_Y": "RearRight_RadarPos_Y",
    "RearRight_RadarPos_Z": "RearRight_RadarPos_Z",
    "RearRightPitchNear": "RearRightPitchNear",
    "RearRight_RollNear": "RearRight_RollNear",
    "RearRight_YawNear": "RearRight_YawNear",
    "RearRight_ConnectorDiretion": "RearRight_ConnectorDirection",
    "RearRight_INSTALL_ANGLE": "RearRight_INSTALL_ANGLE",
    "FrontLeft_RadarPos_X": "FrontLeft_RadarPos_X",
    "FrontLeft_RadarPos_Y": "FrontLeft_RadarPos_Y",
    "FrontLeft_RadarPos_Z": "FrontLeft_RadarPos_Z",
    "FrontLeft_PitchNear": "FrontLeft_PitchNear",
    "FrontLeft_RollNear": "FrontLeft_RollNear",
    "FrontrLeft_YawNear": "FrontLeft_YawNear",
    "FrontLeft_ConnectorDiretion": "FrontLeft_ConnectorDirection",
    "FrontRight_RadarPos_X": "FrontRight_RadarPos_X",
    "FrontRight_RadarPos_Y": "FrontRight_RadarPos_Y",
    "FrontRight_RadarPos_Z": "FrontRight_RadarPos_Z",
    "FrontRight_PitchNear": "FrontRight_PitchNear",
    "FrontRight_RollNear": "FrontRight_RollNear",
    "FrontrRight_YawNear": "FrontRight_YawNear",
    "FrontRight_ConnectorDiretion": "FrontRight_ConnectorDirection",
    "reserve1": "reserve1",
    "起始频率": "StartFrequency",
    "带宽": "Bandwidth",
    "上升沿": "RampUpTime",
    "下降沿": "RampDownTime",
    "周期": "ChirpPeriod",
    "chirp数": "ChirpNumber",
    "adc采样频率": "ADCSampleFreq",
    "adc采样开始时间": "ADCSampleStart",
    "adc采样结束时间": "ADCSampleEnd",
    "距离维FFT个数": "RangeFFTSize",
    "速度维FFT个数": "VelocityFFTSize",
    "cfarpk使能": "CFARPeakEnable",
    "cfar-距离分区1": "CFARRangeZone1",
    "cfar-距离分区2": "CFARRangeZone2",
    "cfar-距离分区3": "CFARRangeZone3",
    "cfar-阈值1": "CFARThreshold1",
    "cfar-阈值2": "CFARThreshold2",
    "cfar-阈值3": "CFARThreshold3",
    "cfar-阈值4": "CFARThreshold4",
    "cfar-阈值5": "CFARThreshold5",
    "cfar-阈值6": "CFARThreshold6",
    "cfar-阈值7": "CFARThreshold7",
    "cfar-阈值8": "CFARThreshold8",
    "解速度模糊使能": "VelocityDeblurEnable",
    "解速度模糊延时": "VelocityDeblurDelay",
    "解速度模糊q值": "VelocityDeblurQ",
    "S起始频率": "S_StartFrequency",
    "S带宽": "S_Bandwidth",
    "S上升沿": "S_RampUpTime",
    "S下降沿": "S_RampDownTime",
    "S周期": "S_ChirpPeriod",
    "Schirp数": "S_ChirpNumber",
    "Sadc采样频率": "S_ADCSampleFreq",
    "Sadc采样开始时间": "S_ADCSampleStart",
    "Sadc采样结束时间": "S_ADCSampleEnd",
    "S距离维FFT个数": "S_RangeFFTSize",
    "S速度维FFT个数": "S_VelocityFFTSize",
    "Scfarpk使能": "S_CFARPeakEnable",
    "Scfar-距离分区1": "S_CFARRangeZone1",
    "Scfar-距离分区2": "S_CFARRangeZone2",
    "Scfar-距离分区3": "S_CFARRangeZone3",
    "Scfar-阈值1": "S_CFARThreshold1",
    "Scfar-阈值2": "S_CFARThreshold2",
    "Scfar-阈值3": "S_CFARThreshold3",
    "Scfar-阈值4": "S_CFARThreshold4",
    "Scfar-阈值5": "S_CFARThreshold5",
    "Scfar-阈值6": "S_CFARThreshold6",
    "Scfar-阈值7": "S_CFARThreshold7",
    "Scfar-阈值8": "S_CFARThreshold8",
    "S解速度模糊使能": "S_VelocityDeblurEnable",
    "S解速度模糊延时": "S_VelocityDeblurDelay",
    "S解速度模糊q值": "S_VelocityDeblurQ",
    "假点1使能": "FalseAlarm1Enable",
    "假点1所属雷达ID": "FalseAlarm1RadarID",
    "假点1速度上限": "FalseAlarm1VelUpper",
    "假点1速度下限": "FalseAlarm1VelLower",
    "假点1距离上限": "FalseAlarm1RangeUpper",
    "假点1距离下限": "FalseAlarm1RangeLower",
    "假点1角度上限": "FalseAlarm1AngleUpper",
    "假点1角度下限": "FalseAlarm1AngleLower",
    "假点2使能": "FalseAlarm2Enable",
    "假点2所属雷达ID": "FalseAlarm2RadarID",
    "假点2速度上限": "FalseAlarm2VelUpper",
    "假点2速度下限": "FalseAlarm2VelLower",
    "假点2距离上限": "FalseAlarm2RangeUpper",
    "假点2距离下限": "FalseAlarm2RangeLower",
    "假点2角度上限": "FalseAlarm2AngleUpper",
    "假点2角度下限": "FalseAlarm2AngleLower",
    "假点3使能": "FalseAlarm3Enable",
    "假点3所属雷达ID": "FalseAlarm3RadarID",
    "假点3速度上限": "FalseAlarm3VelUpper",
    "假点3速度下限": "FalseAlarm3VelLower",
    "假点3距离上限": "FalseAlarm3RangeUpper",
    "假点3距离下限": "FalseAlarm3RangeLower",
    "假点3角度上限": "FalseAlarm3AngleUpper",
    "假点3角度下限": "FalseAlarm3AngleLower",
    "假点4使能": "FalseAlarm4Enable",
    "假点4所属雷达ID": "FalseAlarm4RadarID",
    "假点4速度上限": "FalseAlarm4VelUpper",
    "假点4速度下限": "FalseAlarm4VelLower",
    "假点4距离上限": "FalseAlarm4RangeUpper",
    "假点4距离下限": "FalseAlarm4RangeLower",
    "假点4角度上限": "FalseAlarm4AngleUpper",
    "假点4角度下限": "FalseAlarm4AngleLower",
    "假点5使能": "FalseAlarm5Enable",
    "假点5所属雷达ID": "FalseAlarm5RadarID",
    "假点5速度上限": "FalseAlarm5VelUpper",
    "假点5速度下限": "FalseAlarm5VelLower",
    "假点5距离上限": "FalseAlarm5RangeUpper",
    "假点5距离下限": "FalseAlarm5RangeLower",
    "假点5角度上限": "FalseAlarm5AngleUpper",
    "假点5角度下限": "FalseAlarm5AngleLower",
    "假点6使能": "FalseAlarm6Enable",
    "假点6所属雷达ID": "FalseAlarm6RadarID",
    "假点6速度上限": "FalseAlarm6VelUpper",
    "假点6速度下限": "FalseAlarm6VelLower",
    "假点6距离上限": "FalseAlarm6RangeUpper",
    "假点6距离下限": "FalseAlarm6RangeLower",
    "假点6角度上限": "FalseAlarm6AngleUpper",
    "假点6角度下限": "FalseAlarm6AngleLower",
    "标定抽值": "CalibrationSampleValue",
    "标定起始速度": "CalibrationStartSpeed",
    "标定栅栏点数": "CalibrationFencePoints",
    "标定有效帧数": "CalibrationValidFrames",
    "标定方差设置": "CalibrationVarianceSetting",
    "卡尔曼距离噪声方差": "KalmanRangeNoiseVariance",
    "卡尔曼速度噪声方差": "KalmanVelocityNoiseVariance",
    "卡尔曼角度噪声方差": "KalmanAngleNoiseVariance",
    "标定yawrate": "CalibrationYawRate",
    "卡尔曼滤波机动因子1": "KalmanManeuverFactor1",
    "卡尔曼滤波机动因子2": "KalmanManeuverFactor2",
}


def main():
    csv_file = "./data/rh/RecordData.csv"

    raw_code = ""
    phy_code = ""
    convert_code = ""
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        hex_str = ""
        for row in reader:
            number = row["SerialNo"]
            name = row["Name"].strip()
            name = config_name_map[name]
            if "reserve" in name:
                name = f"reserve_{number}"
            data_type = int(row["DataType"])
            value = row["Val"]
            size = int(row["DataSize"])
            factor = float(row["Factor"])
            factor = factor if factor != 0 else 1  # Avoid division by zero
            offset = float(row["Offset"])

            raw_name = "RhConfigRaw"
            phy_name = "RhConfigPhy"
            match data_type:
                case 0:  # int8_t
                    raw_type = "int8_t"
                    assert size == 1, f"{name} int8_t should have size 1"
                case 1:  # uint8_t
                    raw_type = "uint8_t"
                    assert size == 1, f"{name} uint8_t should have size 1"
                case 2:  # int16_t
                    raw_type = "int16_t"
                    assert size == 2, f"{name} int16_t should have size 2"
                case 3:  # uint16_t
                    raw_type = "uint16_t"
                    assert size == 2, f"{name} uint16_t should have size 2"
                case 4:  # int32_t
                    raw_type = "int32_t"
                    assert size == 4, f"{name} int32_t should have size 4"
                case 5:  # uint32_t
                    raw_type = "uint32_t"
                    assert size == 4, f"{name} uint32_t should have size 4"
                case 6:  # float
                    map = {1: "uint8_t", 2: "uint16_t", 4: "uint32_t"}
                    raw_type = map[size]
                    assert size in [1, 2, 4], f"{name} float should have size 2 or 4"
                case 7:  # string
                    raw_type = "char"
                case default:
                    raise ValueError(f"{name}: Unsupported data type: {data_type}")

            if data_type >= 0 and data_type <= 5:
                phy_type = raw_type
                convert = f"phy->{name} = raw->{name}"
                type_arr_size = ""
            elif data_type == 6:
                phy_type = "float"
                convert = f"phy->{name} = (raw->{name} * {factor}) + {offset}"
                type_arr_size = ""
            else:
                phy_type = "char"
                convert = f"memcpy(phy->{name}, raw->{name}, {size})"
                type_arr_size = f"[{size}]"

            raw_code += f"{raw_type} {name}{type_arr_size};\n"
            phy_code += f"{phy_type} {name}{type_arr_size};\n"
            convert_code += f"{convert};\n"

            if data_type == 7:  # string
                hex_value = value.encode("ascii").hex()
            else:  # int or float
                value = round((float(value) - offset) / factor)
                # Handle negative values using two's complement
                if value < 0:
                    value = (1 << (size * 8)) + value
                hex_value = value.to_bytes(size, byteorder="little").hex()
            hex_str += hex_value.ljust(size * 2, "0")

    with open("./data/output/rh_config_c.c", "w+") as file:
        raw_code = f"typedef struct {{\n{raw_code}}} {raw_name}Type;\n\n"
        phy_code = f"typedef struct {{\n{phy_code}}} {phy_name}Type;\n\n"
        convert_code = (
            f"static inline void RhConfigConvert({raw_name}Type *raw, {phy_name}Type *phy) {{\n{convert_code}}}"
        )
        def_code = f"extern {raw_name}Type {raw_name};\nextern {phy_name}Type {phy_name};\n\n"
        file.write("#include <stdint.h>\n")
        file.write("#include <string.h>\n")
        file.write(raw_code)
        file.write(phy_code)
        file.write(def_code)
        file.write(convert_code)

    hex_bytes = bytearray.fromhex(hex_str)

    ht = hex_tool.HexTool()
    ht.add_segment(0x000C0000, hex_bytes)

    ht.print_summary()
    ht.make_hex("./data/output/rh_config.hex")


if __name__ == "__main__":
    main()
